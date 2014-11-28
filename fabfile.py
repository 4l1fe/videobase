# coding: utf-8

import os
import sys
import re
import json
import fabtools

from time import time
from fabric.api import env, roles, run, settings, sudo, cd, local, require, get, put
from fabric.contrib.files import exists

from subprocess import Popen, PIPE

LOCAL_DOCKER_HOST_TEMPLATE = "localhost:{}"
LOCAL_DOCKER_PASS_TEMPLATE = "root@{}".format(LOCAL_DOCKER_HOST_TEMPLATE)


common_packages = [
    'python', 'build-essential', 'python-dev',
    'python-setuptools', 'python-pip', 'git', 'python-virtualenv', 'postgresql'
]

env.git_clone = 'git@git.aaysm.com:developers/videobase.git'

####################################################################
# Environments

def localhost_env():
    "Use the local virtual server"
    env.hosts = ['localhost']
    env.user = 'tumani1'
    env.project_name = 'videobase2'
    env.path = '/home/%(user)s/workspace/%(project_name)s' % env
    env.env = '/home/%(user)s/venv' % env
    env.current_path = '%(path)s/current' % env
    env.releases_path = '%(path)s/releases' % env
    env.req_dir = 'deploy'
    env.services = ['supervisor', 'nginx']
    env.configs = '/home/%(user)s/configs' % env
    env.pip = '%(env)s/bin/pip' % env
    env.python = '%(env)s/bin/python' % env
    env.shell = '/bin/bash -c'

def production_env():
    "Use the actual webserver"
    env.hosts = ['www.example.com']
    env.user = 'username'
    env.project_name = 'videobase2'
    env.path = '/var/www/%(project_name)s' % env
    env.env = '/home/%(user)s/venv' % env
    env.current_path = '%(path)s/current' % env
    env.releases_path = '%(path)s/releases' % env
    env.req_dir = 'deploy'
    env.services = ['supervisor', 'nginx']
    env.configs = '/home/%(user)s/configs' % env
    env.pip = '%(env)s/bin/pip' % env
    env.python = '%(env)s/bin/python' % env
    env.shell = '/bin/bash -c'


def install_common_packages():
    """
    Установка основных общих системных пакетов
    """
    fabtools.deb.update_index()
    fabtools.deb.install(globals()['common_packages'])


def install_all_sys_packages():
    """
    Установка системных пакетов
    """

    if not 'current_release' in env:
        releases()

    run('cat %(sys_file)s | xargs sudo apt-get install -y ' % {
        'sys_file': os.path.join(env.current_release, env.req_dir, 'system.txt')
    })


def install_npm_packages():
    """
    Установка NodeJS пакетов
    """

    if not 'current_release' in env:
        releases()

    run('cat %(sys_file)s | xargs sudo npm install ' % {
        'sys_file': os.path.join(env.current_release, env.req_dir, 'node.txt')
    })


def releases():
    """
    Список релизов, которые были сделаны
    """

    env.releases = sorted(run('ls -x %(releases_path)s' % env).split())

    if len(env.releases) >= 1:
        env.current_revision = env.releases[-1]
        env.current_release = "%(releases_path)s/%(current_revision)s" % env

    if len(env.releases) > 1:
        env.previous_revision = env.releases[-2]
        env.previous_release = "%(releases_path)s/%(previous_revision)s" % env


def checkout(branch=None):
    """
    Клонирование проекта
    """

    env.current_release = "%(releases_path)s/%(time).0f" % {
        'releases_path': env.releases_path,
        'time': time()
    }

    with cd(env.releases_path):
        env.git_branch = 'master'
        if not branch is None:
            env.git_branch = branch

        run("git clone --depth=1 -b %(git_branch)s %(git_clone)s %(current_release)s" % env)



def update_env(install_node_pkg=False, config_path = None):
    """
    Обновление python окружения
    """

    require('hosts', provided_by=[localhost_env, production_env])

    if not 'current_release' in env:
        releases()

    # Установка остальных системных пакетов
    install_all_sys_packages()

    # Установка NodeJS пакетов
    if install_node_pkg:
        install_npm_packages()

    # Проверка окружения
    if not fabtools.python.virtualenv_exists(env.env):
        fabtools.python.create_virtualenv(env.env)

    with cd(env.current_release):
        # Установка python пакетов

        with cd(env.current_release):
                run("mv configs configs_from_repo")
                run("ln -s %(configs)s configs" % {
                    'configs': env.configs
                })

        with fabtools.python.virtualenv(env.env):
            run('%(pip)s install -r %(path)s' % {
                'pip': env.pip,
                'path': os.path.join(env.current_release, env.req_dir, 'requirements.txt'),
            })

            # Создаем конфиг для supervisor
            create_supervisor_config()


def symlink():
    """
    Устанавливаем символические ссылки
    """

    require('hosts', provided_by=[localhost_env, production_env])

    if not 'current_release' in env:
        releases()

    run('ln -nfs %(current_release)s %(current_path)s' % env)


def restart_services():
    """
    Перезапуск всех сервисов проекта
    """

    require('hosts', provided_by=[])
    for service in env.get('services', [docker_env,localhost_env, production_env]):

        fabtools.service.restart(service)


def setup():
    """
    """

    require('hosts', provided_by=[docker_env,localhost_env, production_env])

    if not fabtools.files.is_dir(env.path):
        run('/bin/mkdir {dir}'.format(dir=env.path))

    run('mkdir -p %(path)s/{releases,current}' % env)

    install_common_packages()

    # Init Postgres User
    if not fabtools.postgres.user_exists('pgadmin'):
         fabtools.postgres.create_user(
             name='pgadmin', password='qwerty',
             createdb=True, createrole=True, superuser=True
         )
 
    # Init Postgres DB
    if not fabtools.postgres.database_exists('videobase'):
         fabtools.postgres.create_database(
             name='videobase', owner='pgadmin'
         )


def migrate(app_name=''):
    """
    Исполнение миграций
    """

    require('hosts', provided_by=[localhost_env, production_env])

    if not 'current_release' in env:
        releases()

    with cd(env.current_release):
        run('%(python)s manage.py migrate %(app_name)s' % {
            'python': env.python,
            'app_name': app_name,
        })


def create_supervisor_config():
    """
    Генерируем конфиг для supervisor
    """

    require('hosts', provided_by=[localhost_env, production_env])

    if not 'current_release' in env:
        releases()

    run('%(python)s manage.py generate_robots_config' % {
        'python': env.python,
    })


def deploy(branch=None, install_node_pkg=False, use_migrate=True):
    require('hosts', provided_by=[docker_env,localhost_env, production_env])
    require('path')

    restart_services()

    setup()
    checkout(branch)
    update_env(install_node_pkg)
    symlink()

    if use_migrate:
        migrate()

    restart_services()


def deploy_version(version):
    """
    Развертывание специальной версии
    """

    require('hosts', provided_by=[localhost_env, production_env])
    require('path')

    if not 'current_release' in env:
        releases()

    if version in env.releases:
        pass
        # with cd(env.path):
        #     env.current_release = "%(releases_path)s/%(version)s" % {
        #         'releases_path': env.releases_path,
        #         'version': version
        #     }
        #
        # restart_services()


def rollback():
    """
    Откат релиза до предыдушего
    """

    require('hosts', provided_by=[localhost_env, production_env])

    if not 'current_release' in env:
        releases()

    if len(env.releases) >= 2:
        env.current_release = env.releases[-1]
        env.previous_revision = env.releases[-2]

        env.current_release = "%(releases_path)s/%(current_revision)s" % {
            'releases_path': env.releases_path,
            'current_revision': env.current_revision
        }
        env.previous_release = "%(releases_path)s/%(previous_revision)s" % {
            'releases_path': env.releases_path,
            'previous_revision': env.previous_revision
        }

        run("rm %(current_path)s; ln -s %(previous_release)s %(current_path)s && rm -rf %(current_release)s" % {
            'current_release': env.current_release,
            'previous_release': env.previous_release,
            'current_path': env.current_path
        })

    restart_services()


def delete_old_releases():
    """
    Удаляем старые релизы
    """

    require('hosts', provided_by=[localhost_env, production_env])

    if not 'current_release' in env:
        releases()

    if len(env.releases) > 3:
        directories = env.releases
        directories.reverse()
        del directories[4:]

        releases()

def get_docker_container_hashes():
    p = Popen('docker ps -q -a', stdout = PIPE, shell = True)
    return  p.communicate()[0].strip().split()

def get_container_data(hashes):
    p2 = Popen("docker inspect {}".format(' '.join(hashes)), stdout = PIPE, shell=True)
    data = json.loads(p2.communicate()[0])
    return data

def get_docker_ports():

    ports = dict ((d['internal'],d["external"]) for d in  [m.groupdict() for m in re.finditer('(?P<external>\d+)->(?P<internal>\d+)',  Popen("docker ps | grep test_sshd", shell= True, stdout = PIPE).communicate()[0])])

    return ports


def docker_env():
    "Use the docker"
    env.user = 'root'
    env.hosts = env.hosts if env.hosts else []
    env.passwords=env.passwords if env.passwords else {}
    env.project_name = 'videobase'
    env.path = '/var/www/%(project_name)s' % env
    env.env = '/root/venv' % env
    env.current_path = '%(path)s/current' % env
    env.releases_path = '%(path)s/releases' % env
    env.req_dir = 'deploy'
    env.services = ['supervisor', 'nginx', 'nginx', 'postgresql']
    env.pip = '%(env)s/bin/pip' % env
    env.python = '%(env)s/bin/python' % env
    env.shell = '/bin/bash -c'
    env.configs = '/root/configs/' % env


def init_docker():

    print "Checking if image alredy built"
    p = Popen(['docker.io images -q eg_sshd',], shell = True, stdout = PIPE)

    hashes = None
    if not p.communicate()[0]:
        print "Couldn't find eg_sshd image. Building one now. Please wait"
        p = Popen(['docker.io build -t eg_sshd ./deploy/',], shell = True, stdout = PIPE)
        while p.poll() is None:
            output = p.stdout.readline()
            print output,

    else:
        print "Found image, Checking if container..."

        hashes = get_docker_container_hashes()


    if hashes:

        data = get_container_data(hashes)

        if u'/test_sshd' in [d['Name'] for d in data]:

            test_sshd = next( d for d in data if d['Name'] == '/test_sshd')

            if test_sshd['State']['Running']:
                print "Container already running"
            else:
                print "Starting container"
                p = Popen(['docker.io start test_sshd',], shell=True)
                p.wait()

        else:
            print "Creating new container"
            p = Popen(['docker run -d -P --name test_sshd eg_sshd',], shell = True)
            p.wait()

    else:
        print "Creating new container"
        p = Popen(['docker run -d -P --name test_sshd eg_sshd',], shell = True)
        p.wait()

def modify_local_nginx(ports):

    abspath = os.path.expanduser('~/nginx-docker.conf')
    if os.path.exists(abspath):
        print "Found local nginx config at {}".format(abspath)
    else:
        raise NameError("Expected local nginx config at {}. Found none".format(abspath))

    with open(abspath) as df:
        data = df.read()

    modified = re.sub('localhost[:](?P<port>[0-9]+)','localhost:{}'.format(ports['80']),data, flags=re.DOTALL)

    with open(abspath,'w') as df:
        df.write(modified)


def modify_supervisor():
    with cd(env.current_release):
        run('{} deploy/update_supervisor.py'.format(env.python))
    run("supervisorctl update")
    run("supervisorctl restart all")

def npm_packets():
    with cd(env.current_release):
        run("npm install jade zerorpc")


def set_nginx_config():

    if exists('/etc/nginx/sites-enabled/vsevi.conf'):
        run('rm /etc/nginx/sites-enabled/vsevi.conf')

    with cd(env.current_path):
        run('/root/venv/bin/python deploy/update_nginx_conf.py')
    with cd('/etc/nginx/sites-enabled/'):
        run('ln -s %(config)/vsevi.conf' % {'config': env.current_path})



def local_docker_deploy(*args, **kwargs):

    init_docker()
    ports = get_docker_ports()

    #Workaround for some reason you need to define both of parameters for Fabriq to work
    env.host_string = LOCAL_DOCKER_HOST_TEMPLATE.format(ports['22'])
    env.hosts.append([LOCAL_DOCKER_HOST_TEMPLATE.format(ports['22'])])

    env.passwords.update({LOCAL_DOCKER_PASS_TEMPLATE.format(ports['22']):'test'})

    deploy(*args,**kwargs)

    npm_packets()
    
    modify_supervisor()
    modify_local_nginx(ports)
    local('sudo service nginx restart')

