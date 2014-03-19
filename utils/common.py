# coding: utf-8

import os
from PIL import Image


def get_image_path(instance, filename):
    """
    Return path for image file from instance
    """
    if instance.pk is None:
        return os.path.join(instance.get_upload_to, filename)
    else:
        return os.path.join(instance.get_upload_to, str(instance.pk), filename)


def get_thumbnail_url(image_url, size=60):
    """
    Return thumbnail url
    """
    thumbs_part = 'thumbs_' + str(size)
    image_url_parts = image_url.rsplit('/', 1)
    return image_url_parts[0] + '/' + thumbs_part + '/' + image_url_parts[1]


def get_thumbnail_path(image_path, size=60):
    """
    Create thumbnail directory if not exist and return her path
    """
    thumbs_dir = 'thumbs_' + str(size)
    dirname, filename = os.path.split(image_path)
    dirname = os.path.join(dirname, thumbs_dir)

    if not os.path.exists(dirname):
        os.mkdir(dirname, 0755)

    return os.path.join(dirname, filename)


def create_thumbnail(image_path, size=60):
    """
    Create thumbnail by image
    """
    thumb_path = get_thumbnail_path(image_path, size)
    delete_thumbnail(image_path, size)
    img = Image.open(image_path)
    img.thumbnail((size, size), Image.ANTIALIAS)
    img.save(thumb_path)


def delete_thumbnail(image_path, size=60):
    """
    Delete thumbnail if he already exist
    """
    thumb_path = get_thumbnail_path(image_path, size)
    if os.path.exists(thumb_path):
        os.remove(thumb_path)


def check_callable_function(obj, method):
    """
    checks whether the object has to be a method
    """
    callable_flag = False
    try:
        if hasattr(obj, method) and getattr(obj, method):
            callable_flag = True
    except:
        pass

    return callable_flag
