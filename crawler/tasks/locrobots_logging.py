# coding: utf-8
import json
import datetime

from celery import Task

from djcelery.models import TaskMeta
from djcelery.picklefield import decode
from djcelery.views import task_status

from apps.robots.models.robots_logs import RobotsInfoLogging
from apps.robots.models.robots_mail_list import RobotsMailList
from apps.users.tasks import  send_statistic_to_mail
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


def write_logs_to_table(robot_name, location_ids):
    RobotsInfoLogging.objects.create(robot_name=robot_name, locations=location_ids, log_time=datetime.date.today())


def get_locations_list_from_locations_dict_list(locations_dict_list):
    res_list = []
    for location in locations_dict_list:
        res_list.append(location['location_id'])
    return res_list


def fill_robots_locations_logs_to_table(locations_dict):
    try:
        if len(locations_dict['info']) == 0:
            return
        print create_structures_string(locations_dict['type'], get_locations_list_from_locations_dict_list(locations_dict['info']))
        write_logs_to_table(locations_dict['type'], get_locations_list_from_locations_dict_list(locations_dict['info']))
    except Exception, e:
        pass


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


def collect_logs(date=datetime.datetime.now().date()):
    robo_dict={}
    for robolog in RobotsInfoLogging.objects.all():
        if robolog.log_time.date() == date:
            if robolog.robot_name in robo_dict:
                robo_dict[robolog.robot_name] += ", " + robolog.locations
            else:
                robo_dict[robolog.robot_name] = robolog.locations
    set_zero_for_not_present_in_table_robots(robo_dict)
    return robo_dict


def set_zero_for_not_present_in_table_robots(robo_dict):
    for robot in ROBOTS_LIST:
        if robot not in robo_dict:
            robo_dict[robot] = ''
    for robot in sites_crawler.keys():
        if robot not in robo_dict:
            robo_dict[robot] = ''


def create_one_email_report_str_for_statistic(robo_name, location_ids):
    result = "<p> <span>Robot </span> <span>{0}</span> <span> returned {1}</span> <span> locations: {2}</span> </p>".format(robo_name, len(location_ids.split()), location_ids)
    return result


def send_statistic_to_email_for_each_robot():
    str_for_send = ""
    robo_dict = collect_logs()
    for key, value in robo_dict.iteritems():
        one_report_str = create_one_email_report_str_for_statistic(key, value)
        str_for_send += one_report_str
    send_message_for_all_recipients(str_for_send, "robots logs")


def send_message_for_all_recipients(message, subject):
    to = []
    for item in RobotsMailList.objects.all():
        to.append(item.email)
    if len(to) == 0:
        return
    kwrg = {
            'subject': subject,
            'text': message,
            'to': to,
           }
    send_statistic_to_mail.apply_async(kwargs=kwrg)