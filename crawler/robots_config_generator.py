# coding: utf-8
from sys import executable
from os.path import abspath
from crawler.robots_type_checker import RobotsTypeChecker


def generate_robots_config(directory='.', user='developers', file_name='robots_config.conf', hostname='vsevi.ru'):
    d = abspath(directory)
    u, fn, hn = user, file_name, hostname  # сокращение
    worker_command = lambda robot_name: executable + " manage.py celery worker -c 1 -Q {0} -n {0}.%h ".format(robot_name)
    main_worker_command = executable + " manage.py celery worker -c 1"
    beat_worker_command = executable + " manage.py celery beat --pidfile=/tmp/celerybeat.pid"


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
redirect_stderr=true'''
    generate_program = lambda program_name, command, dir_, u: template_pr.format(program_name, command, dir_, u)

    rtc = RobotsTypeChecker()
    lr_list = rtc.get_locrobots_list()
    dr_list = rtc.get_datarobots_list()
    cr_list = ['cast_sportbox_robot', 'cast_liverussia_robot', 'cast_championat_robot', 'cast_khl_robot', 'cast_ntv_plus_robot']
    adr_list = ['robot_beat', 'robot_statistics_email', 'robot_notification_email', 'robot_newsletter_email',
                'robot_avatar', 'location_saver', 'thor']

    with open(fn, 'w') as file:
        for robot in lr_list:
            command = worker_command(robot)
            file.write(generate_program(robot, command, d, u))
            file.write("\n")

        for robot in dr_list:
            command = worker_command(robot)
            file.write(generate_program(robot, command, d, u))
            file.write("\n")

        for robot in cr_list:
            command = worker_command(robot)
            file.write(generate_program(robot, command, d, u))
            file.write("\n")

        for robot in adr_list:
            command = worker_command(robot)
            file.write(generate_program(robot, command, d, u))
            file.write("\n")

        file.write(generate_program('main_worker', main_worker_command, d, u))
        file.write("\n")

        file.write(generate_program('beat_worker', beat_worker_command, d, u))
        file.write("\n")

        file.write(generate_group('locrobots', ','.join(lr_list)))
        file.write("\n")

        file.write(generate_group('datarobots', ','.join(dr_list)))
        file.write("\n")

        file.write(generate_group('castrobots', ','.join(cr_list)))
        file.write("\n")

        file.write(generate_group('additionalrobots', ','.join(['main_worker']+adr_list)))
        file.write("\n")

    return fn