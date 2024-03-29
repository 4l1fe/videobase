# coding: utf-8
from fabric.api import env, roles, run, settings, sudo, cd, local
import fabric
from fabtools import require
import fabtools
import os
from string import Template

env.hosts = ['188.226.191.166',]
env.user = 'root'
env.shell = "/bin/bash -c"


def setup():

    # Require some Debian/Ubuntu packages
    require.deb.packages([
        'libxml2-dev',
        'mercurial',
        'memcached',
        'libmemcached-dev',
        'zlib1g-dev',
        'libssl-dev',
        'python-dev',
        'build-essential',
        'libjpeg-dev',
        'libfreetype6-dev',
        'zlib1g-dev',
        'libpng12-dev',
        'libpq-dev'
    ])


def init_db():
    """
    Создает базу данных и пользователя для основного сайта

    """
    with settings(sudo_user = "postgres"):
        sudo('''echo "CREATE USER pgadmin WITH PASSWORD 'qwerty'; CREATE DATABASE videobase; GRANT ALL PRIVILEGES ON DATABASE videobase to pgadmin;" | psql''')


def init_test_db():
    """
    Создает базу данных и пользователя для тест сайта

    """
    with settings(sudo_user = "postgres"):
        sudo('''echo "CREATE USER pgadmin WITH PASSWORD 'qwerty'; CREATE DATABASE videobase_test; GRANT ALL PRIVILEGES ON DATABASE videobase_test to pgadmin;" | psql''')


def populate_test_db():
    """
    Заполняет тестовую базу данных из sql_dump который идет с кодом
    """
    with cd('/var/www/videobase_test/sql_dump'):
        with settings(sudo_user = "postgres"):
            sudo('''psql -d videobase_test -f $(ls -1 *.sql | head -1)''')
def local_db_reset():
    '''
    Перезаписать локальную базу из репозитория
    '''
    local('''echo "DROP DATABASE videobase;" |  sudo -u postgres psql''')
    local('''echo "CREATE USER pgadmin WITH PASSWORD 'qwerty'; CREATE DATABASE videobase; GRANT ALL PRIVILEGES ON DATABASE videobase to pgadmin;" |  sudo -u postgres psql''')
    local("""cd sql_dump && sudo -u postgres psql -d videobase -f $(ls -1 *.sql | head -1)""")
    local('''echo "DROP DATABASE test_base;" | sudo -u postgres psql ''')
    local('''echo "CREATE DATABASE test_base; ALTER DATABASE test_base OWNER TO pgadmin;" |  sudo -u postgres psql''')


def setup_system_libraries():

    '''
    '''


    pass


def deploy_test_code():
    """
    Обновляет или создает код для тестового сайта


    ВНИМАНИЕ Скрипт редактирует db.ini для того чтобы ссылаться на тестовую базу данных

    """
    with settings(sudo_user = "www-data"):
        with cd('/var/www'):

            result = str(sudo('ls -1')).strip()
            filtered_array=[s for s in result.split('\r\n') if s=='test_base']

            if filtered_array:
                #sudo("cd videobase_test; git checkout configs/db.ini")
                #sudo("cd videobase_test; cat configs/db.ini")
                sudo('cd test_base;git pull')
                #sudo("cd videobase_test/configs/ && sed -i 's/videobase/videobase_test/g' db.ini")
                #sudo("cd videobase_test; cat configs/db.ini")
            else:
                sudo('git clone git@git.aaysm.com:developers/videobase.git test_base')
                sudo("cd test_base/configs/ && cp db.ini.example db.ini && sed -i 's/videobase/test_base/g' db.ini")


def restart_all():
    """
    Перезапуск всех процессов

    """

    sudo('service supervisor stop')
    sudo('sleep 10;service supervisor start')
    sudo('service nginx stop')
    sudo('service nginx start')


def initial_test_deploy():
    """
    Последовательность команд для выгрузки на новую машину

    """

    init_test_db()
    deploy_test_code()
    populate_test_db()


def delete_test_db():
    """
    Удалить тестовую базу данных

    """

    with cd('/var/lib/postgresql'):
        with settings(sudo_user = "postgres"):
            sudo('''echo "DROP DATABASE videobase_test;" | psql''')


def refresh_test_requirements():

    with settings(sudo_user = "www-data"):
        with cd('/var/www/videobase_test/'):
            sudo('/home/virtualenv/videobase_test/bin/pip install -r requirements.txt')


def status():

    for k in fabric.state.output:
        fabric.state.output[k] = False
    fabric.state.output['user']=True

    with settings(warn_only=True):
        print('SUPERVISOR \n')
        print(run("supervisorctl status"))
        print("\n NGINX \n")
        print(run("ps aux |grep nginx"))

        print("\nIs login page is shown on videobase.test.aaysm.com/admin  ? ")
        print(bool(run('''wget -qO- --header="Host: videobase.test.aaysm.com" localhost:80/admin/ |grep Password | wc -l''')))


    for k in fabric.state.output:
        fabric.state.output[k] = True
    fabric.state.output['debug']=False


def db_migrate_test(appname=''):

    '''
    Выполняет миграцию базы данных для приложения (app в терминах Django) если указано, или просто m

    '''

    with settings(sudo_user = "www-data"):
        with cd('/var/www/videobase_test/'):
            sudo('/home/virtualenv/videobase_test/bin/python manage.py migrate %s --no-initial-data' % appname)


def collect_static():
    """
    build/update static files
    """
    with settings(sudo_user = "www-data"):
        with cd('/var/www/videobase_test/'):
            sudo('/home/virtualenv/videobase_test/bin/python manage.py collectstatic --dry-run --noinput')


def deploy():

    """
    Обновить код и перезапустить процессы

    """
    deploy_test_code()
    restart_all()
    status()


def project_deploy():
    '''
    Обновить весь код

    '''
    setup()
    deploy_test_code()
    refresh_test_requirements()
    db_migrate_test()
    collect_static()
    restart_all()
    status()


def db_flush_test():

    """
    Перезаписать тестовую базу данных из дампа
    """
    delete_test_db()
    init_test_db()
    populate_test_db()


def init_if_not_exists_task():
    """
    Обновить если пользователя еще нет.
    Оставил как заготовку
    """

    with settings(sudo_user = "postgres"):
        with cd('/var/lib/postgresql'):
            if not (str(sudo('''echo "select rolname from pg_roles where rolname = 'pgadmin';" |psql -tA''')).strip()):
                init_db()


def scheme():

    local('python ./manage.py graph_models -a -g -o current.png')



def show_scheme():
    scheme()
    local('feh current.png')


def generate_robots_conf(python_interpreter = None, videobase_dir = None, user= None):


    if python_interpreter is None:
        python_interpreter = local("which python",capture=True)
    if videobase_dir is None:
        videobase_dir = os.path.abspath('.')
    if user is None:
        user = local('whoami',capture=True)


    robots_list = local('python manage.py list_robots',capture=True).split()
    print robots_list

    template = Template("""[program:$name]
command=$interpreter manage.py robot_start --site $name
process_name=%(program_name)s ; process_name expr (default %(program_name)s)
numprocs=1 ; number of processes copies to start (def 1)
directory=$workdir ; directory to cwd to before exec (def no cwd)
umask=022 ; umask for process (default None)
autostart=false ; start at supervisord start (default: true)
autorestart=false ; retstart at unexpected quit (default: true)
startretries=1 ; max # of serial start failures (default 3)
user=$user ; setuid to this UNIX account to run the program
redirect_stderr=true ; redirect proc stderr to stdout (default false)
stdout_logfile=/var/log/$name.log""")


    config = '\n'.join(template.substitute({'interpreter':python_interpreter,
        'user':user,
        'workdir': videobase_dir,
        'name': robot_name
        }) for robot_name in robots_list)

    return config


def set_local_robot_config():
    with open('configs/robots.conf','w') as fw:
        fw.write(generate_robots_conf())

    local('sudo cp configs/robots.conf /etc/supervisor/conf.d/robots.conf')
    local('sudo service supervisor restart')

