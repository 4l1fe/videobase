# coding: utf-8

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from videobase.celery import app

from apps.films.models import Films, Persons, UsersFilms, UsersPersons
from apps.films.constants import APP_PERSONFILM_SUBS_TRUE, APP_USERFILM_SUBS_TRUE
from apps.users.constants import APP_NOTIFICATION_TEMPLATE,\
    APP_NOTIFICATION_EMAIL_SUBJECT, FILM_O, PERSON_O


@app.task(name="confirm_register", queue="send_mail")
def send_template_mail(subject, tpl_name, context, to):
    tpl = render_to_string(tpl_name, context)
    msg = EmailMultiAlternatives(subject=subject, to=to)
    msg.attach_alternative(tpl, 'text/html')
    msg.send()


@app.task(name="notification", queue="notification")
def notification(id_, type_):
    if type_ not in (FILM_O, PERSON_O):
        raise ValueError("Not valid argument")

    tpl_name = APP_NOTIFICATION_TEMPLATE[type_]
    subject = APP_NOTIFICATION_EMAIL_SUBJECT[type_]
    if type_ == FILM_O:
        model_obj = Films
        model_user = UsersFilms

        query = {
            'film': id_,
            'subscribed': APP_USERFILM_SUBS_TRUE,
        }
    else:
        model_obj = Persons
        model_user = UsersPersons
        query = {
            'person': id_,
            'subscribed': APP_PERSONFILM_SUBS_TRUE,
        }

    try:
        obj = model_obj.objects.get(id=id_)
        context = {'object': obj}
        to = model_user.objects.filter(**query).exclude(user__email='').values_list("user__email", flat=True)
        kw = {
            'subject': subject,
            'tpl_name': tpl_name,
            'to': to,
            'context': context,
        }
        send_template_mail.apply_async(kwargs=kw)

    except:
        pass
