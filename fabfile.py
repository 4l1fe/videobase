# coding: utf-8

import os
import time
import fabtools

from string import Template
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
    """

    from time import time
    env.current_release = "%(releases_path)s/%(time).0f" % {'releases_path': env.releases_path, 'time': time()}

    with cd(env.releases_path):
        env.git_branch = 'master'
        if not branch is None:
            env.git_branch = branch

        run("git clone -b %(git_branch)s %(git_clone)s %(current_release)s" % env)


def update_env(install_node_pkg=False):
    """
    Обновление python окружения
    """

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

    if not 'current_release' in env:
        releases()

    with cd(env.current_release):
        run('%(python)s manage.py migrate %(app_name)s --no-initial-data --delete-ghost-migrations' % {
            'app_name': app_name,
            'current_release': env.current_release,
        })


def supervisor_config():
    """
    Генерируем конфиг для supervisor
    """

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
    pass









# def init_db():
#     """
#     Создает базу данных и пользователя для основного сайта
#     """
#
#     with settings(sudo_user="postgres"):
#         sudo("""echo "CREATE USER pgadmin WITH PASSWORD 'qwerty'; CREATE DATABASE videobase; GRANT ALL PRIVILEGES ON DATABASE videobase to pgadmin;" | psql""")
#
#
# def populate_test_db():
#     """
#     Заполняет тестовую базу данных из sql_dump который идет с кодом
#     """
#
#     with cd('/var/www/videobase_test/sql_dump'):
#         with settings(sudo_user="postgres"):
#             sudo("""psql -d videobase_test -f $(ls -1 *.sql | head -1)""")
#
#
# def local_db_reset():
#     """
#     Перезаписать локальную базу из репозитория
#     """
#
#     local("""echo "DROP DATABASE videobase;" | sudo -u postgres psql""")
#     local("""echo "CREATE USER pgadmin WITH PASSWORD 'qwerty'; CREATE DATABASE videobase; GRANT ALL PRIVILEGES ON DATABASE videobase to pgadmin;" | sudo -u postgres psql""")
#     local("""cd sql_dump && sudo -u postgres psql -d videobase -f $(ls -1 *.sql | head -1)""")
#     local("""echo "DROP DATABASE test_base;" | sudo -u postgres psql """)
#     local("""echo "CREATE DATABASE test_base; ALTER DATABASE test_base OWNER TO pgadmin;" | sudo -u postgres psql""")
#
#
# def deploy_test_code():
#     """
#     Обновляет или создает код для тестового сайта
#     ВНИМАНИЕ Скрипт редактирует db.ini для того чтобы ссылаться на тестовую базу данных
#     """
#
#     with settings(sudo_user="www-data"):
#         with cd('/var/www'):
#             result = str(sudo('ls -1')).strip()
#             filtered_array = [s for s in result.split('\r\n') if s == 'test_base']
#
#             if len(filtered_array):
#                 #sudo("cd videobase_test; git checkout configs/db.ini")
#                 #sudo("cd videobase_test; cat configs/db.ini")
#                 sudo('cd test_base;git pull')
#                 #sudo("cd videobase_test/configs/ && sed -i 's/videobase/videobase_test/g' db.ini")
#                 #sudo("cd videobase_test; cat configs/db.ini")
#             else:
#                 sudo('git clone git@git.aaysm.com:developers/videobase.git test_base')
#                 sudo("cd test_base/configs/ && cp db.ini.example db.ini && sed -i 's/videobase/test_base/g' db.ini")
#
#
# def delete_test_db():
#     """
#     Удалить тестовую базу данных
#     """
#
#     with cd('/var/lib/postgresql'):
#         with settings(sudo_user="postgres"):
#             sudo('''echo "DROP DATABASE videobase_test;" | psql''')
#
#
# def refresh_test_requirements():
#     with settings(sudo_user="www-data"):
#         with cd('/var/www/videobase_test/'):
#             sudo('/home/virtualenv/videobase_test/bin/pip install -r requirements.txt')
#
#
# def status():
#     for k in fabric.state.output:
#         fabric.state.output[k] = False
#
#     fabric.state.output['user'] = True
#
#     with settings(warn_only=True):
#         print('SUPERVISOR \n')
#         print(run("supervisorctl status"))
#         print("\n NGINX \n")
#         print(run("ps aux | grep nginx"))
#
#         print("\nIs login page is shown on videobase.test.aaysm.com/admin?")
#         print(bool(run('''wget -qO- --header="Host: videobase.test.aaysm.com" localhost:80/admin/ | grep Password | wc -l''')))
#
#     for k in fabric.state.output:
#         fabric.state.output[k] = True
#
#     fabric.state.output['debug'] = False
#
#
# def db_migrate_test(appname=""):
#     """
#     Выполняет миграцию базы данных для приложения (app в терминах Django) если указано, или просто m
#     """
#
#     with settings(sudo_user="www-data"):
#         with cd('/var/www/videobase_test/'):
#             sudo('/home/virtualenv/videobase_test/bin/python manage.py migrate %s --no-initial-data' % appname)
#
#
# def collect_static():
#     """
#     build/update static files
#     """
#
#     with settings(sudo_user="www-data"):
#         with cd('/var/www/videobase_test/'):
#             sudo('/home/virtualenv/videobase_test/bin/python manage.py collectstatic --dry-run --noinput')
#
#
# # def db_flush_test():
# #     """
# #     Перезаписать тестовую базу данных из дампа
# #     """
# #
# #     delete_test_db()
# #     init_test_db()
# #     populate_test_db()
#
#
# def scheme():
#     local('python ./manage.py graph_models -a -g -o current.png')
#
#
# def show_scheme():
#     scheme()
#     local('feh current.png')
#
# def set_local_robot_config():
#     with open('configs/robots.conf', 'w') as fw:
#         fw.write(generate_robots_conf())
#
#     local('sudo cp configs/robots.conf /etc/supervisor/conf.d/robots.conf')
#     local('sudo service supervisor restart')
