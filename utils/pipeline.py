# coding: utf-8
import StringIO
import requests
from PIL import Image

from apps.users.models import UsersPics

from django.core.files.uploadedfile import InMemoryUploadedFile

GET_IMAGE_URLS = {
    'vk-oauth2': lambda response: response.get('photo_max'),
    'facebook': lambda response: u'http://graph.facebook.com/{0}/picture?type=large'.format(response.get('id')),
    'twitter': lambda response: response['profile_image_url'].replace('_normal', '_bigger') if 'profile_image_url' in response and 'default_profile' in response['profile_image_url'] else None,
    'google-oauth2': lambda response: response.get('image'),
}


def get_email(details, user, *args, **kwargs):
    email = details.get('email')
    if user and user.email:
        email = user.email
    details.update({'email': email})


def get_firstname(details, user=None, *args, **kwargs):
    first_name = details.get('first_name')
    last_name = details.get('last_name')
    if first_name and last_name:
        first_name = u"{0} {1}".format(first_name, last_name)
    elif first_name is None and last_name:
        first_name = last_name
    if user and user.first_name:
        first_name = user.first_name

    details.update({'first_name': first_name})


def load_avatar(strategy, response, user, *args, **kwargs):
    image_url = None
    if user:
        image_url = GET_IMAGE_URLS[strategy.backend.name](response)
    if image_url:
        # Get image
        image_string = requests.get(image_url).content
        buff_png = StringIO.StringIO(image_string)
        # Convert image from png to jpg
        png = Image.open(buff_png)
        jpg = Image.new("RGB", png.size, (255, 255, 255))
        jpg.paste(png, (0, 0))
        buff_jpg = StringIO.StringIO()
        jpg.save(buff_jpg, "JPEG")

        # Save image
        memory_file_name = "users_pics.jpg"
        memory_file = InMemoryUploadedFile(buff_jpg, None, memory_file_name, 'image/jpeg', buff_jpg.len, None)
        users_pics = UsersPics(user=user)
        users_pics.save()
        users_pics.image.save(memory_file_name, memory_file)
        users_pics.save()
        profile = user.profile
        if not profile.userpic_id:
            profile.userpic_type = strategy.backend.name
            profile.userpic_id = users_pics.id
            profile.save()


