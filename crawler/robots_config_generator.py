# coding: utf-8
from sys import executable
from os.path import abspath


def generate_robots_config(directory='.', user='developers', file_name='robots_config.conf'):
    d = abspath(directory)
    u, fn = user, file_name  # сокращение
    worker_command = lambda robot_name: executable + " manage.py celery worker -c 1 -Q {0} -n {0}.%%h ".format(robot_name)
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

    with open(fn, 'w') as file:
        for robot in lt_list:
            command = worker_command(robot)
            file.write(generate_program(robot, command, d, u))
            file.write("\n")

        for robot in dt_list:
            command = worker_command(robot)
            file.write(generate_program(robot, command, d, u))
            file.write("\n")

        for robot in ct_list:
            command = worker_command(robot)
            file.write(generate_program(robot, command, d, u))
            file.write("\n")

        for robot in adnt_list:
            command = worker_command(robot)
            file.write(generate_program(robot, command, d, u))
            file.write("\n")

        file.write(generate_program('main', main_command, d, u))
        file.write("\n")

        file.write(generate_program('beat', beat_command, d, u))
        file.write("\n")

        file.write(generate_group('locrobots', ','.join(lt_list)))
        file.write("\n")

        file.write(generate_group('datarobots', ','.join(dt_list)))
        file.write("\n")

        file.write(generate_group('castrobots', ','.join(ct_list)))
        file.write("\n")

        file.write(generate_group('additionalrobots', ','.join(adnt_list)))
        file.write("\n")

    return fn