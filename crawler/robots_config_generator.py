# coding: utf-8
from sys import executable
from crawler.robots_type_checker import RobotsTypeChecker


def queue_command(robot_name):
    return executable + " manage.py celery worker -Q {}".format(robot_name)


def main_queue_command():
    return executable + " manage.py celery worker"


def generate_group(group_name, process_list):
    template = '''
[group:{}]
programs={}'''.format(group_name, process_list)
    return template


def generate_program(program_name, command):
    template = '''
[program:{}]
command={}
process_name=%(program_name)s ;
directory=/var/www/videobase/ ;
umask=022 ;
startretries=1 ;
user=www-data ;
redirect_stderr=true'''.format(program_name, command)
    return template


def generate_robots_config(file_name='robots_config.conf'):
    rtc = RobotsTypeChecker()
    lr_list = rtc.get_locrobots_list()
    dr_list = rtc.get_datarobots_list()
    sr_list = rtc.get_support_robots()
    cr_list = rtc.get_casts_robot()

    with open(file_name, 'w') as file:
        for robot in lr_list:
            command = queue_command(robot)
            file.write(generate_program(robot, command))
            file.write("\n")

        for robot in dr_list:
            command = queue_command(robot)
            file.write(generate_program(robot, command))
            file.write("\n")

        for robot in cr_list:
            command = queue_command(robot)
            file.write(generate_program(robot, command))
            file.write("\n")

        command = queue_command('location_saver')
        file.write(generate_program('location_saver', command))
        file.write("\n")

        command = queue_command('thor')
        file.write(generate_program('thor', command))
        file.write("\n")

        command = main_queue_command()
        file.write(generate_program('main_worker', command))
        file.write("\n")

        file.write(generate_group('locrobots', ','.join(lr_list)))
        file.write("\n")

        file.write(generate_group('datarobots', ','.join(dr_list)))
        file.write("\n")

        file.write(generate_group('castsrobots', ','.join(cr_list)))
        file.write("\n")

        file.write(generate_group('supportrobots', ','.join(sr_list)))
        file.write("\n")

    return file_name