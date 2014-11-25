# coding: utf-8

from crawler.tasks.datarobots_tasks import (kinopoisk_films, kinopoisk_set_paster,
                                            create_due_refresh_tasks, parse_kinopoisk_news,
                                            find_trailer, trailer_commands)
from crawler.tasks.casts_tasks import (sportbox_update, liverussia_update, championat_update,
                                       khl_update, ntv_plus_update)
from crawler.tasks.save_location_task import save_location_from_robo_task
from crawler.tasks.robot_logs_tasks import send_robots_statistic_to_email
