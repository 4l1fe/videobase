# coding: utf-8
from videobase.celery import app
from crawler.tasks.locrobots_logging import send_statistic_to_email_for_each_robot

__author__ = 'vladimir'


@app.task(name='send_robots_logs_to_email')
def send_robots_statistic_to_email():
    send_statistic_to_email_for_each_robot()

