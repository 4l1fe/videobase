# coding: utf-8
from sys import executable
from os.path import abspath
from videobase.settings import CAST_QUEUE, MAIL_QUEUE, NOTIFY_QUEUE, DATA_QUEUE, LOCATION_QUEUE_P, LOCATION_QUEUE_S


def generate_robots_config(directory='.', user='developers', file_name='robots_config.conf'):
    d = abspath(directory)
    u, fn = user, file_name  # сокращение
    worker_command = lambda queue, worker_name: executable + " manage.py celery worker -c 1 -Q {0} -n {1}.%%h ".format(queue, worker_name)
    main_command = executable + " manage.py celery worker -c 1 -n main.%%h"
    beat_command = executable + " manage.py celery beat --pidfile=/tmp/celerybeat.pid"

    template_pr = '''[program:{}]
command={}
process_name=%(program_name)s ;
directory={} ;
umask=022 ;
startretries=1 ;
user={} ;
redirect_stderr=true ;
stdout_logfile=/var/log/%(program_name)s.log'''
    generate_program = lambda program_name, command, dir_, u: template_pr.format(program_name, command, dir_, u)

    with open(fn, 'w') as file:
        
        file.write(generate_program('main', main_command, d, u))
        file.write("\n\n")

        file.write(generate_program('beat', beat_command, d, u))
        file.write("\n\n")

        file.write(generate_program(CAST_QUEUE, worker_command(CAST_QUEUE, CAST_QUEUE+'_worker'), d, u))
        file.write("\n\n")

        file.write(generate_program(MAIL_QUEUE, worker_command(MAIL_QUEUE, MAIL_QUEUE+'_worker'), d, u))
        file.write("\n\n")

        file.write(generate_program(NOTIFY_QUEUE, worker_command(NOTIFY_QUEUE, NOTIFY_QUEUE+'_worker'), d, u))
        file.write("\n\n")

        file.write(generate_program(DATA_QUEUE, worker_command(DATA_QUEUE, DATA_QUEUE + '_worker'), d, u))
        file.write("\n\n")

        file.write(generate_program(LOCATION_QUEUE_S, worker_command(LOCATION_QUEUE_S, LOCATION_QUEUE_S+'_worker'), d, u))
        file.write("\n\n")

        file.write(generate_program(LOCATION_QUEUE_P, worker_command(LOCATION_QUEUE_P, LOCATION_QUEUE_P+'_worker'), d, u))
        file.write("\n\n")

    return fn