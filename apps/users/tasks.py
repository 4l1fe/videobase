# coding: utf-8

import StringIO
import textwrap
import requests
from PIL import Image

from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.core.files.uploadedfile import InMemoryUploadedFile

from utils.noderender import render_page

from videobase.celery import app

from apps.films.models import Films, Persons, UsersFilms, UsersPersons
from apps.films.constants import APP_PERSONFILM_SUBS_TRUE, APP_USERFILM_SUBS_TRUE

from apps.users.models import User, UsersPics
from apps.users.constants import APP_NOTIFICATION_TEMPLATE,\
    APP_NOTIFICATION_EMAIL_SUBJECT, FILM_O, PERSON_O, EMAIL_HEADERS


@app.task(name="send_template_mail", queue="mail")
def send_template_mail(subject, context, to, tpl_name=None, use_render=True, jade_render=False, **kwargs):
    """
    Очередь отправки сообщений
    """

    if isinstance(to, basestring):
        to = [to]
    
    if use_render:
        if jade_render:
            text_email = render_page(tpl_name, context, False)
        else:
            text_email = render_to_string(tpl_name, context)
    else:
        text_email = context

    text_email = '\r\n'.join(textwrap.wrap(text_email.encode('utf-8').encode('base64'), 76))
    msg = EmailMessage(subject, text_email, to=to, headers=EMAIL_HEADERS)
    msg.content_subtype = 'html'
    msg.send()


@app.task(name="notification", queue="notify")
def film_notification(id_, type_, **kwargs):
    """
    Очередь обработка момента, когда появилось событие подписки на фильм или на персону
    """

    if type_ not in (FILM_O, PERSON_O):
        raise ValueError("Not valid argument")

    define_id = id_ if type_ == FILM_O else kwargs['child_obj']
    o_film = Films.objects.get(id=define_id)

    kw = {
        'subject': APP_NOTIFICATION_EMAIL_SUBJECT[type_],
        'tpl_name': APP_NOTIFICATION_TEMPLATE[type_],
        'context': {
            'film': {
                'id': o_film.id,
                'name': o_film.name
            }
        }
    }

    if type_ == FILM_O:
        model_user = UsersFilms
        query = {
            'film': id_,
            'subscribed': APP_USERFILM_SUBS_TRUE,
        }

    else:
        model_user = UsersPersons
        o_person = Persons.objects.get(id=id_)
        kw['context']['person'] = {
            'id': o_person.id,
            'name': o_person.name
        }

        query = {
            'person': id_,
            'subscribed': APP_PERSONFILM_SUBS_TRUE,
        }

    # Выборка почтовых адресов
    list_email = model_user.objects.filter(**query).exclude(user__email='').values_list("user__email", flat=True)

    # Send email from list
    for item in list_email:
        kw.update({'to': item})
        send_template_mail.apply_async(kwargs=kw)


@app.task(name="get_avatar", queue="load")
def avatar_load(image_url, type_, user_id=None, **kwargs):
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
