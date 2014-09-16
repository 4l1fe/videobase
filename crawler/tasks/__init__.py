# coding: utf-8

from crawler.tasks.locrobots_tasks import amediateka_robot_start, pltask, \
    viaplay_robot_start, launch_individual_film_site_task, age_weighted_robot_launcher

from crawler.tasks.datarobots_tasks import kinopoisk_films,\
    kinopoisk_set_paster, imdb_robot_start,\
    create_due_refresh_tasks, parse_kinopoisk_news, find_trailer,\
    trailer_commands

from crawler.tasks.save_location_task import save_location_from_robo_task
