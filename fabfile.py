from fabric.api import env,roles, run, settings, sudo, cd

env.hosts = ['188.226.191.166',]
env.user = 'root'
env.shell= "/bin/bash -c"

def init_db():
    with settings(sudo_user = "postgres"):
        sudo('''echo "CREATE USER pgadmin WITH PASSWORD 'qwerty'; CREATE DATABASE videobase; GRANT ALL PRIVILEGES ON DATABASE videobase to pgadmin;" | psql''')

def init_test_db():
    with settings(sudo_user = "postgres"):
        sudo('''echo "CREATE USER pgadmin WITH PASSWORD 'qwerty'; CREATE DATABASE videobase_test; GRANT ALL PRIVILEGES ON DATABASE videobase_test to pgadmin;" | psql''')
    
def populate_test_db():
    with cd('/var/www/videobase_test/sql_dump'):
        run('chmod 644 $(ls -1 *.sql | head -1)')
        with settings(sudo_user = "postgres"):
            sudo('''psql -f $(ls -1 *.sql | head -1)''')

        
def deploy_test_code():
    with settings(sudo_user = "www-data"):
        with cd('/var/www'):
            print([s for s in str(sudo('ls -1')).strip().split('\r\n') if s=='videobase_test'])
            if [s for s in str(sudo('ls -1')).strip().split('\r\n') if s=='videobase_test']:
                sudo('cd videobase_test;git pull')
            else:
                sudo('git clone /var/git/videobase.git/ videobase_test')

                
def initial_test_deploy():
    init_test_db()
    deploy_test_code()
    populate_test_db()
                

def delete_test_db():
    with cd('/var/lib/postgresql'):
        with settings(sudo_user = "postgres"):
            sudo('''echo "DROP DATABASE videobase_test;" | psql''')

            
def refresh_code():
    run('cd /var/www/videobase; git pull ')

def restart():
    run('service nginx restart')

    
def deploy():
    refresh_code()
    restart()


def init_if_not_exists_task():
    with settings(sudo_user = "postgres"):
        with cd('/var/lib/postgresql'):
            if not ((sudo('''echo "select rolname from pg_roles where rolname = 'pgadmin';" |psql -tA''')).strip()):
                init_db()
 
