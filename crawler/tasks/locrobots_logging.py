# coding: utf-8
from email.mime.text import MIMEText
import json
import smtplib
from celery import Task
import datetime
from django.forms.models import model_to_dict
import djcelery
from djcelery.models import TaskMeta
from djcelery.picklefield import decode
from djcelery.views import task_status

__author__ = 'vladimir'


def write_logs_to_console():
    for task in TaskMeta.objects.all():
        result = task_status(None, task.task_id)
        print "decoded", decode(task.meta)
        js = json.loads(result.content)
        task_result = js['task']['result']
        if task_result is not None:
            print result


def create_structures_string(self, robot_name, location_ids):
    #print "Robot ", robot_name + "returned ", len(location_ids), "locations: ", location_ids
    return "Robot {} returned {} locations: {} ".format(str(robot_name), len(location_ids), location_ids)


def send_logs_to_email(logs):
    sender = ''
    recivers = ['']
    msg = MIMEText(logs)
    msg['Subject'] = 'Logs for %s date' % datetime.date.today()
    #msg['From'] = sender
    #msg['To'] = reciver

    s = smtplib.SMTP('localhost')
    s.sendmail(sender, recivers, msg.as_string())
    s.quit()


class DebugTask(Task):
    abstract = True

    def after_return(self, *args, **kwargs):
        try:
            print create_structures_string(args[1][0], args[1][1])
        except:
            pass
