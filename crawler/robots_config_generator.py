# coding: utf-8
from sys import executable
from os.path import abspath
from videobase.settings import DATAROBOTS_SCHEDULE, LOCATIONROBOTS_SCHEDULE, CASTROBOT_SCHEDULE, CELERYBEAT_SCHEDULE, \
    CAST_QUEUE, MAIL_QUEUE, NOTIFY_QUEUE, DATA_QUEUE, LOCATION_QUEUE_P, LOCATION_QUEUE_S


def generate_robots_config(directory='.', user='developers', file_name='robots_config.conf'):
    d = abspath(directory)
    u, fn = user, file_name  # сокращение
    worker_command = lambda queues, worker_name: executable + " manage.py celery worker -c 1 -Q {0} -n {1}.%%h ".format(queues, worker_name)
    main_command = executable + " manage.py celery worker -c 1"
    beat_command = executable + " manage.py celery beat --pidfile=/tmp/celerybeat.pid"

    template_gr = '''
[group:{}]
programs={}'''
    generate_group = lambda group_name, processes: template_gr.format(group_name, processes)

    template_pr = '''
[program:{}]
command={}
process_name=%(program_name)s ;
directory={} ;
umask=022 ;
startretries=1 ;
user={} ;
redirect_stderr=true ;
stdout_logfile=/var/log/%(program_name)s.log'''
    generate_program = lambda program_name, command, dir_, u: template_pr.format(program_name, command, dir_, u)

    lt_list = []
    dt_list = []
    ct_list = []
    adnt_list = []

    for key, value in LOCATIONROBOTS_SCHEDULE.iteritems():
        lt_list += [key]

    for key, value in DATAROBOTS_SCHEDULE.iteritems():
        dt_list += [key]

    for key, value in CASTROBOT_SCHEDULE.iteritems():
        ct_list += [key]

    for key, value in CELERYBEAT_SCHEDULE.iteritems():
        ct_list += [key]

    with open(fn, 'w') as file:

        file.write(generate_program('main', main_command, d, u))
        file.write("\n")

        file.write(generate_program('beat', beat_command, d, u))
        file.write("\n")

        cast_queue = [CAST_QUEUE]
        mail_notify_queue = [MAIL_QUEUE, NOTIFY_QUEUE]
        data_queue = [DATA_QUEUE]
        location_queue = [LOCATION_QUEUE_S, LOCATION_QUEUE_P]

        file.write(generate_program(CAST_QUEUE, worker_command(','.join(cast_queue), CAST_QUEUE+'_worker'), d, u))
        file.write("\n")

        file.write(generate_program(MAIL_QUEUE+'_'+NOTIFY_QUEUE, worker_command(','.join(mail_notify_queue), MAIL_QUEUE+'_'+NOTIFY_QUEUE+'_worker'), d, u))
        file.write("\n")

        file.write(generate_program(DATA_QUEUE, worker_command(','.join(data_queue), DATA_QUEUE + '_worker'), d, u))
        file.write("\n")

        file.write(generate_program('locations', worker_command(','.join(location_queue), 'locations_worker'), d, u))
        file.write("\n")

    return fn