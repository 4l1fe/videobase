# coding: utf-8

import os
import time
import fabtools

from string import Template
from fabric.api import env, roles, run, settings, sudo, cd, local, require

# env.roledefs = {
#     'production': ['developers@5.9.17.109'],
#     'staging': ['developers@188.226.191.166'],
#     'test': ['tumani1@127.0.0.1'],
# }

common_packages = [
    'python', 'build-essential', 'python-dev',
    'python-setuptools', 'python-pip'
]

env.git = 'git@git.aaysm.com:developers/videobase.git'

####################################################################
# Environments

def localhost_env():
    "Use the local virtual server"
    env.hosts = ['localhost']
    env.user = 'tumani1'
    env.project_name = 'videobase2'
    env.path = '/home/%(user)s/workspace/%(project_name)s' % env
    env.env = '/home/%(user)s/venv' % env
    env.virtualhost_path = env.path

def production_env():
    "Use the actual webserver"
    env.hosts = ['www.example.com']
    env.user = 'username'
    env.path = '/var/www/%(project_name)s' % env
    env.virtualhost_path = env.path

# def production_env():
#     """Окружение для продакшена"""
#     # env.key_filename = [os.path.join(os.environ['HOME'], '.ssh', 'git_example_org')] # Локальный путь до файла с ключами
#     env.user = 'developers'  # На сервере будем работать из под пользователя "git"
#     env.project_root = '/home/developers/videobase2'  # Путь до каталога проекта (на сервере)
#     env.shell = '/bin/bash -c'  # Используем шелл отличный от умолчательного (на сервере)
#     env.python = '/home/developers/venv/bin/python'  # Путь до python (на сервере)
#     env.env = '/home/developers/venv'
#
#
# def test_env():
#     """Окружение для локальной площадки"""
#     env.run = local
#     env.host_string = 'localhost'
#     env.user = 'tumani1'
#     env.project_root = '/home/tumani1/workspace/videobase'
#     env.shell = '/bin/bash -c'
#     env.python = '/home/tumani1/virtualenv/videobase/bin/python'
#     env.env = '/home/tumani1/virtualenv/videobase/'
#     env.use_ssh_config = False
#
#
# def staging_env():
#     """Окружение для тестовой площадки"""
#     # env.key_filename = [os.path.join(os.environ['HOME'], '.ssh', 'git_example_org')] # Локальный путь до файла с ключами
#     env.user = 'developers'
#     env.project_root = '/home/developers/videobase2'
#     env.shell = '/bin/bash -c'
#     env.python = '/home/developers/venv/bin/python'
#     env.env = '/home/developers/venv'


####################################################################
def deploy(git_stash=True, **kwargs):
    # roledefs = {
    #     'production': ['developers@5.9.17.109'],
    #     'staging': ['developers@188.226.191.166'],
    #     'test': ['tumani1@127.0.0.1'],
    # }


    # if not envir in roledefs:
    #     raise ValueError('This enviroment "{env}" does exist'.format(env=envir))

    # # Init enviroment
    # envir_func = '{env_name}_env'.format(env_name=envir)
    # globals()[envir_func]()

    require('hosts', provided_by=[localhost_env, production_env])
    require('path')

    env.release = time.strftime('%d.%m.%y %H:%M')

    # Install common packages
    fabtools.deb.install(globals()['common_packages'])

    # Проверка окружения
    if not fabtools.python.virtualenv_exists(env.env):
        fabtools.python.create_virtualenv(env.env)

    # Проверка директории проекта
    init_proj = False
    if not fabtools.files.is_dir(env.path):
        init_proj = True
        run('/bin/mkdir {dir}'.format(dir=env.path))

        # Clone project by git
        fabtools.git.clone(env.git, path=env.path)

    with cd(env.path):
        # Update project
        if not init_proj:
            if git_stash:
                run('git stash save "Uncommitted changes before update operation at {time}"'.format(
                    time=env.release
                ))

            run('git pull')

        # Require some Debian/Ubuntu packages
        sys_packages = []
        append = sys_packages.append
        with open('system.txt', 'r') as package:
            append(package)

        if len(sys_packages):
            fabtools.deb.install(sys_packages)

        # Require Node packages
        sys_packages = []
        append = sys_packages.append
        with open('node.txt', 'r') as package:
            append(package)

        if len(sys_packages):
            fabtools.nodejs.install_package()

        if init_proj:
            # Init Postgres User
            if not fabtools.postgres.user_exists():
                fabtools.postgres.create_user(
                    name='pgadmin', password='qwerty',
                    createdb=True, createrole=True,
                )

            # Init Postgres DB
            if not fabtools.postgres.database_exists('videobase'):
                fabtools.postgres.create_database(
                    name='videobase', owner='pgadmin'
                )

        # Require a Python package
        with fabtools.python.virtualenv(env.env):
            run('{pip} install --upgrade -r {filepath}'.format(
                pip=env.pip,
                filepath=os.path.join(env.project_root, 'requirements.txt')
            ))

            # Сбор статики
            run('{python} manage.py collectstatic --dry-run --noinput'.format(
                python=env.python
            ))

            if init_proj:
                run('{python} manage.py migrate syncdb'.format(python=env.python))

            # Миграции
            run('{python} manage.py migrate --no-initial-data'.format(
                python=env.python
            ))

            # Restart сервисов
            restart_services()


#
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


def restart_services():
    """
    Перезапуск всех процессов
    """

    list_services = ['supervisor', 'nginx']
    for service in list_services:
        fabtools.service.restart(service)


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
# # def deploy():
# #     """
# #     Обновить код и перезапустить процессы
# #     """
# #
# #     deploy_test_code()
# #     restart_all()
# #     status()
#
#
# def project_deploy():
#     """
#     Обновить весь код
#     """
#
#     setup()
#     deploy_test_code()
#     refresh_test_requirements()
#     db_migrate_test()
#     collect_static()
#     restart_all()
#     status()
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
#
# def generate_robots_conf(python_interpreter=None, videobase_dir=None, user=None):
#     if python_interpreter is None:
#         python_interpreter = local("which python", capture=True)
#
#     if videobase_dir is None:
#         videobase_dir = os.path.abspath('.')
#
#     if user is None:
#         user = local('whoami', capture=True)
#
#     robots_list = local('python manage.py list_robots', capture=True).split()
#     print robots_list
#
#     template = Template("""[program:$name]
# command=$interpreter manage.py robot_start --site $name
# process_name=%(program_name)s ; process_name expr (default %(program_name)s)
# numprocs=1 ; number of processes copies to start (def 1)
# directory=$workdir ; directory to cwd to before exec (def no cwd)
# umask=022 ; umask for process (default None)
# autostart=false ; start at supervisord start (default: true)
# autorestart=false ; retstart at unexpected quit (default: true)
# startretries=1 ; max # of serial start failures (default 3)
# user=$user ; setuid to this UNIX account to run the program
# redirect_stderr=true ; redirect proc stderr to stdout (default false)
# stdout_logfile=/var/log/$name.log""")
#
#     config = '\n'.join(template.substitute({
#         'interpreter': python_interpreter,
#         'user': user,
#         'workdir': videobase_dir,
#         'name': robot_name
#     }) for robot_name in robots_list)
#
#     return config
#
#
# def set_local_robot_config():
#     with open('configs/robots.conf', 'w') as fw:
#         fw.write(generate_robots_conf())
#
#     local('sudo cp configs/robots.conf /etc/supervisor/conf.d/robots.conf')
#     local('sudo service supervisor restart')
