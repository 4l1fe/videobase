# coding: utf-8
import json
import datetime

from celery import Task

from djcelery.models import TaskMeta
from djcelery.picklefield import decode
from djcelery.views import task_status
from apps.films.models import Films

from apps.robots.models.robots_logs import RobotsInfoLogging, LocationsCorrectorLogging
from apps.robots.models.robots_mail_list import RobotsMailList
from apps.users.tasks import send_template_mail
from crawler.locrobots import sites_crawler
from videobase.settings import ROBOTS_LIST

__author__ = 'vladimir'


def write_logs_to_console():
    for task in TaskMeta.objects.all():
        result = task_status(None, task.task_id)
        print "decoded", decode(task.meta)
        js = json.loads(result.content)
        task_result = js['task']['result']
        if task_result is not None:
            print result


def create_structures_string(robot_name, location_ids):
    return "Robot {} returned {} locations: {} ".format(str(robot_name), len(location_ids), location_ids)


def write_one_log_to_table(robot_name, location_ids, film_id, is_new_added):
    RobotsInfoLogging.objects.create(robot_name=robot_name, locations=location_ids, films=film_id, is_new_location=is_new_added, log_time=datetime.date.today())
    print "Logged ", location_ids


def get_locations_list_from_locations_dict_list(locations_dict_list):
    res_list = []
    for location in locations_dict_list:
        res_list.append(location['location_id'])
    return res_list


def get_fields_from_locations_dict_list(locations_dict_list):
    res_fields = []
    for location in locations_dict_list:
        res_fields.append(location)
    return res_fields


def fill_robots_locations_logs_to_table(locations_dict):
    try:
        if len(locations_dict['info']) == 0:
            return
        #print create_structures_string(locations_dict['type'], get_fields_from_locations_dict_list(locations_dict['info']))
        write_all_logs_to_table(locations_dict['type'], get_fields_from_locations_dict_list(locations_dict['info']))
    except Exception, e:
        print "Failded logging because ", e.message


def write_all_logs_to_table(robot_name, locs_inormation):
    for loc_inf in locs_inormation:
        loc_id = loc_inf['location_id']
        film_id = loc_inf['film_id']
        is_new = loc_inf['is_new']
        write_one_log_to_table(robot_name, loc_id, film_id, is_new)


#Ф-я для заполнения лога по роботам которые не в стандартной схеме
def fill_log_table_for_not_schema_corresponded_robots(locations_dict):
    fill_robots_locations_logs_to_table(locations_dict)


# Класс для роботов, которые написаны по схеме
class DebugTask(Task):
    abstract = True

    def after_return(self, *args, **kwargs):
        if not args[1]:
            return
        locations_dict = args[1]
        fill_robots_locations_logs_to_table(locations_dict)


def clear_log_table():
    RobotsInfoLogging.objects.all().delete()


def clear_corrector_log_table():
    LocationsCorrectorLogging.objects.all().delete()


def collect_logs(date=datetime.datetime.now().date()):
    robo_dict={}
    for robolog in RobotsInfoLogging.objects.all():
        if robolog.log_time.date() == date:
            robo_info = {
                'loc_id': None,
                'film_id': None,
                'is_new': False
            }
            robo_info['loc_id'] = robolog.locations
            robo_info['film_id'] = robolog.films
            robo_info['is_new'] = robolog.is_new_location
            if robolog.robot_name in robo_dict:
                robo_dict[robolog.robot_name] += [robo_info]
            else:
                robo_dict[robolog.robot_name] = [robo_info]
    set_zero_for_not_present_in_table_robots(robo_dict)
    return robo_dict


def collect_logs_for_deleted_flocations(date=datetime.datetime.now().date()):
    floc_del_dict={}
    for location_log in LocationsCorrectorLogging.objects.all():
        if location_log.log_time.date() == date:
            if location_log.robot_name in floc_del_dict:
                floc_del_dict[location_log.robot_name] += [location_log.films]
            else:
                floc_del_dict[location_log.robot_name] = [location_log.films]

    set_zero_for_not_present_in_table_robots(floc_del_dict)
    return floc_del_dict


def set_zero_for_not_present_in_table_robots(robo_dict):
    for robot in ROBOTS_LIST:
        if robot not in robo_dict:
            robo_dict[robot] = ''
    for robot in sites_crawler.keys():
        if robot not in robo_dict:
            robo_dict[robot] = ''


def create_one_email_report_str_for_statistic(robo_name, robot_informs_list):
    result = "<p> <span>Robot </span> <span>{0}</span> <span> returned {1}</span> <span> locations:".format(robo_name, len(robot_informs_list))

    for robo_info in robot_informs_list:
        if robo_info['is_new']:
            result += "{0} ({1}, {2})".format(robo_info['loc_id'], robo_info['film_id'], "new")
        else:
            result += "{0} ({1})".format(robo_info['loc_id'], robo_info['film_id'])
        result += ", "
    result += "</span> </p>"
    return result


def create_report_for_locations_corrector(robo_name, loc_corrector_film_ids):
    result = "<p> <span>From </span> <span>{0}</span> <span> was deleted {1}</span> <span> films:".format(robo_name, len(loc_corrector_film_ids))
    for film_id in loc_corrector_film_ids:
        f = Films.objects.get(id = film_id)
        result += "({0}, {1}, {2})".format(film_id, f.name.encode("utf8"), str(f.release_date))
        result += ", "
    result += "</span> </p>"
    return result


def send_statistic_to_email_for_each_robot():
    str_for_send = ""
    robo_dict = collect_logs()
    loc_corrector_log = collect_logs_for_deleted_flocations()
    #clear_log_table()
    #clear_corrector_log_table()
    for key, value in robo_dict.iteritems():
        one_report_str = create_one_email_report_str_for_statistic(key, value)
        str_for_send += one_report_str

    for key, value in loc_corrector_log.iteritems():
        one_report_str = create_report_for_locations_corrector(key, value)
        str_for_send += one_report_str

    send_message_for_all_recipients(str_for_send, "robots logs")


def send_message_for_all_recipients(message, subject):
    print "Send messages"

    message = {
        'subject': subject,
        'context': message,
    }

    to = []
    for item in RobotsMailList.objects.all():
        to.append(item.email)

    if not len(to):
        return

    print "Generating task to send message to {}".format(to)

    for t in to:
        message.update({'to': t})
        send_template_mail.apply_async(kwargs=message)
