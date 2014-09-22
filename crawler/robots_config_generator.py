# coding: utf-8
from apps.robots.models import Robots
from sys import executable
from videobase.settings import ROBOTS_LIST

__author__ = 'vladimir'


def create_queue_str(robot_name):
    return executable + " manage.py celery worker -Q {}".format(robot_name)


def create_main_queue_str():
    return executable + " manage.py celery worker"


def generate_process_section_with_parameters(programm_name, command, log_file_name):
    template = '''
[program:{}]
command={}
process_name=%(program_name)s ; process_name expr (default %(program_name)s)
numprocs=1 ; number of processes copies to start (def 1)
directory=/var/www/videobase/ ; directory to cwd to before exec (def no cwd)
umask=022 ; umask for process (default None)
startretries=1 ; max # of serial start failures (default 3)
user=www-data ; setuid to this UNIX account to run the program
redirect_stderr=true ; redirect proc stderr to stdout (default false)
stdout_logfile=/var/log/{}.log'''.format(programm_name, command, log_file_name)
    return template


def generate_config_file():
    result_file_name = ''
    f = open('robots_config.conf', 'w')
    for robot in Robots.objects.all():
        robo_command = create_queue_str(robot.name)
        f.write(generate_process_section_with_parameters(robot.name, robo_command, robot.name))
    for robot in ROBOTS_LIST:
        robo_command = create_queue_str(robot)
        f.write(generate_process_section_with_parameters(robot, robo_command, robot))
    saver_command = create_queue_str('location_saver')
    f.write(generate_process_section_with_parameters('location_saver', saver_command, 'location_saver'))
    thor_command = create_queue_str('thor')
    f.write(generate_process_section_with_parameters('thor', thor_command, 'thor'))
    main_command = create_main_queue_str()
    f.write("\n")
    f.write(generate_process_section_with_parameters('main_worker', main_command, 'main_worker'))
    result_file_name = 'robots_config.conf'
    return result_file_name