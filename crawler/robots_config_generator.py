# coding: utf-8
from sys import executable
from crawler.robots_type_checker import RobotsTypeChecker


def generate_robots_config(directory='.', user='www-data', file_name='robots_config.conf'):
    d, u, fn = directory, user, file_name  # сокращение
    queue_command = lambda robot_name: executable + " manage.py celery worker -Q {}".format(robot_name)
    main_queue_command = lambda: executable + " manage.py celery worker"

    template = '''
    [group:{}]
    programs={}'''
    generate_group = lambda group_name, process_list: template.format(group_name, process_list)

    template = '''
    [program:{}]
    command={}
    process_name=%(program_name)s ;
    directory={} ;
    umask=022 ;
    startretries=1 ;
    user={} ;
    redirect_stderr=true'''
    generate_program = lambda program_name, command, dir_, u: template.format(program_name, command, dir_, u)

    rtc = RobotsTypeChecker()  # отсюда берутся списки роботов
    lr_list = rtc.get_locrobots_list()
    dr_list = rtc.get_datarobots_list()
    sr_list = rtc.get_support_robots()
    cr_list = rtc.get_casts_robot()

    with open(fn, 'w') as file:
        for robot in lr_list:
            command = queue_command(robot)
            file.write(generate_program(robot, command, d, u))
            file.write("\n")

        for robot in dr_list:
            command = queue_command(robot)
            file.write(generate_program(robot, command, d, u))
            file.write("\n")

        for robot in cr_list:
            command = queue_command(robot)
            file.write(generate_program(robot, command, d, u))
            file.write("\n")

        command = queue_command('location_saver')
        file.write(generate_program('location_saver', command, d, u))
        file.write("\n")

        command = queue_command('thor')
        file.write(generate_program('thor', command, d, u))
        file.write("\n")

        command = main_queue_command()
        file.write(generate_program('main_worker', command, d, u))
        file.write("\n")

        file.write(generate_group('locrobots', ','.join(lr_list)))
        file.write("\n")

        file.write(generate_group('datarobots', ','.join(dr_list)))
        file.write("\n")

        file.write(generate_group('castsrobots', ','.join(cr_list)))
        file.write("\n")

        file.write(generate_group('supportrobots', ','.join(sr_list)))
        file.write("\n")

    return fn