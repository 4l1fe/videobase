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

#
#
#
#  'confirm_register'
#  'consolidate_rating'
#  'drugoe_kino_update'
#  'film_info_check_and_correct'
#  'find_trailer_for_film'
#  'get_avatar'
#  'itunes_robot_start'
#  'kinopoisk_films'
#  'kinopoisk_mobile_parse_film'
#  'kinopoisk_news'
#  'kinopoisk_parse_film_by_id'
#  'kinopoisk_persons'
#  'kinopoisk_refresher'
#  'kinopoisk_set_poster'
#  'load_film_from_site'
#  'mail_robot_start'
#  'notification'
#  'parse_news_from_now_ru'
#  'parse_news_from_stream_ru'
#  'parse_news_from_tvzor_ru'
#  'parse_you_tube_movies_ru'
#  'personal_newsletter'
#  'persons_check_and_correct'
#  'persons_films_update_with_indexes'
#  'playfamily_xml'
#  'process_film_on_site'
#  'refresh_sitemap'
#  'save_location'
#  'send_robots_logs_to_email'
#  'send_robots_statistic_to_email'
#  'update_film_rating'
#  'update_ratings'
#  'viaplay_ru_robot_start'
#  'videobase.celery.debug_task'
#  'week_newsletter'
#  'youtube_trailers_all'


    lt_list = ['age_weighted_robot_launch', 'amediateka_ru_robot_start']
    dt_list = ['check_one_film_by_id', 'check_one_person_by_id']
    ct_list = ['cast_notify']
    adnt_list = ['calc_amount_subscribed_to_movie', ]

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

        file.write(generate_group('locrobots', ','.join(lrt_list)))
        file.write("\n")

        file.write(generate_group('datarobots', ','.join(drt_list)))
        file.write("\n")

        file.write(generate_group('castrobots', ','.join(crt_list)))
        file.write("\n")

        file.write(generate_group('additionalrobots', ','.join(adrt_list)))
        file.write("\n")

    return fn