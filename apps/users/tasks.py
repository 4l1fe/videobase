# coding: utf-8
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from celery.task import task


@task(name="confirm_register")
def send_template_mail(subject, tpl_name, context, to):
    tpl = render_to_string(tpl_name, context)
    msg = EmailMultiAlternatives(subject=subject, to=to)
    msg.attach_alternative(tpl, 'text/html')
    msg.send()
