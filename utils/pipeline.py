# coding: utf-8
from apps.users.tasks import avatar_load
from apps.users.models import User
from videobase.settings import SOCIAL_AUTH_VK_PHOTO_FIELD

GET_IMAGE_URLS = {
    'vk-oauth2': lambda response: response.get(SOCIAL_AUTH_VK_PHOTO_FIELD),
    'facebook': lambda response: u'http://graph.facebook.com/{0}/picture?type=large&height=500&width=500'.format(response.get('id')),
    'twitter': lambda response: response['profile_image_url'].replace('_normal', '_bigger') if 'profile_image_url' in response and 'default_profile' in response['profile_image_url'] else None,
    'google-oauth2': lambda response: response.get('image'),
}


def get_email(details, user, response, *args, **kwargs):
    email = details.get('email') or response.get('email')
    unique_email = User.objects.filter(email=email).exists()
    if unique_email:
        if user and user.email:
            email = user.email
        details.update({'email': email})
        if email:
            details.update({'username': email})


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
    if user and strategy.backend.name in GET_IMAGE_URLS:
        try:
            get_image_url = GET_IMAGE_URLS[strategy.backend.name]
            image_url = get_image_url(response)
            avatar_load.apply_async(kwargs=dict(image_url=image_url, type_=strategy.backend.name, user_id=user.id))
        except Exception as e:
            pass



