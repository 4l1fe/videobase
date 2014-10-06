# coding: utf-8
from apps.robots.models import Robots
from sys import executable
from crawler.robots_type_checker import RobotsTypeChecker
from videobase.settings import ROBOTS_LIST

__author__ = 'vladimir'


def create_queue_str(robot_name):
    return executable + " manage.py celery worker -Q {}".format(robot_name)


def create_main_queue_str():
    return executable + " manage.py celery worker"


def generate_group_name(group_name, process_list):
    template = '''
[group:{}]
programs={}'''.format(group_name, process_list)
    return template


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
    robots_type_checker = RobotsTypeChecker()
    result_file_name = ''
    locrobots_group_list = robots_type_checker.get_locrobots_list()
    datarobots_group_list = robots_type_checker.get_datarobots_list()
    supportrobots_group_list = robots_type_checker.get_support_robots()
    f = open('robots_config.conf', 'w')
    for robot in locrobots_group_list: #Robots.objects.all()
        robo_command = create_queue_str(robot)
        f.write(generate_process_section_with_parameters(robot, robo_command, robot))
    for robot in datarobots_group_list: #ROBOTS_LIST
        robo_command = create_queue_str(robot)
        f.write(generate_process_section_with_parameters(robot, robo_command, robot))
    saver_command = create_queue_str('location_saver')
    f.write(generate_process_section_with_parameters('location_saver', saver_command, 'location_saver'))
    thor_command = create_queue_str('thor')
    f.write(generate_process_section_with_parameters('thor', thor_command, 'thor'))
    main_command = create_main_queue_str()
    f.write("\n")
    f.write(generate_process_section_with_parameters('main_worker', main_command, 'main_worker'))
    f.write("\n")
    f.write(generate_group_name('locrobots_group', get_regular_str_from_list(locrobots_group_list)))
    f.write(generate_group_name('datarobots_group', get_regular_str_from_list(datarobots_group_list)))
    f.write(generate_group_name('supportrobots_group', get_regular_str_from_list(supportrobots_group_list)))

    result_file_name = 'robots_config.conf'
    return result_file_name


def get_regular_str_from_list(list):
    res = str(list).replace('[', '')
    res = res.replace(']', '')
    res = res.replace("'", '')
    return res