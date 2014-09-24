# coding: utf-8

import StringIO
import requests
from PIL import Image

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.core.files.uploadedfile import InMemoryUploadedFile

from utils.noderender import render_page

from videobase.celery import app

from apps.films.models import Films, Persons, UsersFilms, UsersPersons
from apps.films.constants import APP_PERSONFILM_SUBS_TRUE, APP_USERFILM_SUBS_TRUE

from apps.users.models import User, UsersPics
from apps.users.constants import APP_NOTIFICATION_TEMPLATE,\
    APP_NOTIFICATION_EMAIL_SUBJECT, FILM_O, PERSON_O


@app.task(name="confirm_register", queue="send_mail")
def send_template_mail(subject, tpl_name, context, to, jade_render=False):
    if jade_render:
        tpl = render_page(tpl_name, context, False)
    else:
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
        to = model_user.objects.filter(**query).exclude(user__email='').values_list("user__email", flat=True)
        kw = {
            'subject': subject,
            'tpl_name': tpl_name,
            'to': to,
            'context': {'object': obj},
        }

        # Send email
        send_template_mail.apply_async(kwargs=kw)
    except Exception, e:
        pass


@app.task(name="send_robots_statistic_to_email", queue="send_mail")
def send_statistic_to_mail(subject, text, to):
    msg = EmailMultiAlternatives(subject=subject, to=to)
    msg.attach_alternative(text, 'text/html')
    msg.send()


@app.task(name="get_avatar", queue="load")
def avatar_load(image_url, type_, user_id=None):
    response = requests.get(image_url)
    if response.status_code == 200:
        buff = StringIO.StringIO(response.content)
        # Convert image from png to jpg
        png_image = Image.open(buff)
        im = Image.new("RGB", png_image.size, (255, 255, 255))
        im.paste(png_image, (0, 0))
        buff = StringIO.StringIO()
        im.save(buff, "JPEG")

        # Save image
        memory_file_name = "users_pics.jpg"
        memory_file = InMemoryUploadedFile(buff, None, memory_file_name, 'image/jpeg', buff.len, None)
        user = User.objects.get(id=user_id)
        users_pics = UsersPics(user=user, type=type_)
        users_pics.save()
        users_pics.image.save(memory_file_name, memory_file)
        users_pics.save()
        profile = user.profile
        if not profile.userpic_id:
            profile.userpic_type = type_
            profile.userpic_id = users_pics.id
            profile.save()
