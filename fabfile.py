# coding: utf-8

import os
import fabtools

from time import time
from fabric.api import env, roles, run, settings, sudo, cd, local, require, get, put


common_packages = [
    'python', 'build-essential', 'python-dev',
    'python-setuptools', 'python-pip'
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

    env.pip = '%(env)s/bin/pip' % env
    env.python = '%(env)s/bin/python' % env
    env.shell = '/bin/bash -c'


def install_common_packages():
    """
    Установка основных общих системных пакетов
    """

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

        run("git clone -b %(git_branch)s %(git_clone)s %(current_release)s" % env)


def update_env(install_node_pkg=False):
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
        with fabtools.python.virtualenv(env.env):
            run('%(pip)s install -r %(path)s' % {
                'pip': env.pip,
                'path': os.path.join(env.current_release, env.req_dir, 'requirements.txt'),
            })

            run('%(python)s manage.py generate_robots_config' % env)


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

    for service in env.get('services', []):
        fabtools.service.restart(service)


def setup():
    """
    """

    require('hosts', provided_by=[localhost_env, production_env])

    if not fabtools.files.is_dir(env.path):
        run('/bin/mkdir {dir}'.format(dir=env.path))

    run('mkdir -p %(path)s/{releases,current}' % env)

    # # Init Postgres User
    # if not fabtools.postgres.user_exists():
    #     fabtools.postgres.create_user(
    #         name='pgadmin', password='qwerty',
    #         createdb=True, createrole=True,
    #     )
    #
    # # Init Postgres DB
    # if not fabtools.postgres.database_exists('videobase'):
    #     fabtools.postgres.create_database(
    #         name='videobase', owner='pgadmin'
    #     )


def migrate(app_name=''):
    """
    Исполнение миграций
    """

    require('hosts', provided_by=[localhost_env, production_env])

    if not 'current_release' in env:
        releases()

    with cd(env.current_release):
        run('%(python)s manage.py migrate %(app_name)s --no-initial-data --delete-ghost-migrations' % {
            'app_name': app_name,
            'current_release': env.current_release,
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


def deploy(branch=None, install_node_pkg=False):
    require('hosts', provided_by=[localhost_env, production_env])
    require('path')

    setup()
    checkout(branch)
    update_env(install_node_pkg)
    symlink()
    migrate()
    restart_services()


def deploy_version(version):
    """
    Развертывание специальной версии
    """

    require('hosts', provided_by=[localhost_env, production_env])
    require('path')

    env.version = version
    with cd(env.path):
        pass

    restart_services()


def rollback():
    """
    Откат релиза до предыдушего
    """

    require('hosts', provided_by=[localhost_env, production_env])

    if not 'current_release' in env:
        releases()

    pass
