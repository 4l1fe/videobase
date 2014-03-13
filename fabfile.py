# coding: utf-8
from fabric.api import env,roles, run, settings, sudo, cd
import fabric

env.hosts = ['188.226.191.166',]
env.user = 'root'
env.shell= "/bin/bash -c"

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

        
def deploy_test_code():
    """
    Обновляет или создает код для тестового сайта


    ВНИМАНИЕ Скрипт редактирует db.ini для того чтобы ссылаться на тестовую базу данных

    """
    with settings(sudo_user = "www-data"):
        with cd('/var/www'):

            result = str(sudo('ls -1')).strip()
            filtered_array=[s for s in result.split('\r\n') if s=='videobase_test']
            
            if filtered_array:
                #sudo("cd videobase_test; git checkout configs/db.ini")
                #sudo("cd videobase_test; cat configs/db.ini")
                sudo('cd videobase_test;git pull')
                #sudo("cd videobase_test/configs/ && sed -i 's/videobase/videobase_test/g' db.ini")
                #sudo("cd videobase_test; cat configs/db.ini")
            else:
                sudo('git clone /var/git/videobase.git/ videobase_test')
                sudo("cd videobase_test/configs/ && cp db.ini.example db.ini && sed -i 's/videobase/videobase_test/g' db.ini")

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
            sudo('/home/virtualenv/videobase_test/bin/python manage.py migrate %s' % appname)
    
def deploy():

    """
    Обновить код и перезапустить процессы

    """
    deploy_test_code()
    db_migrate_test()
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

