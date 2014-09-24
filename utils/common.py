# coding: utf-8

import os
import sys
import traceback
import random
import string
import urllib


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


def list_of(list, key, objects=False, distinct=False):
    """
    Возвращает массив состоящий из значений всех полей key
    в двумерном массиве или в массиве объектов list
    """
    result_list = []
    for item in list:
        if objects:
            value = getattr(item, key)
        else:
            value = item[key]

        result_list.append(value)

    # if distinct:
    #     result_list = list(set(result_list))

    return result_list


def reindex_by(list, key, objects=False):
    """
    Преобразует массив объектов, в масисв с ключем по полю key
    """
    result_dict = {}
    for item in list:
        if objects: k_value = getattr(item, key)
        else: k_value = item[key]
        result_dict[k_value] = item

    return result_dict


def group_by(list, key, objects=False):
    """
    Сгруппировать двумерный массив или массив объектов
    по полю с именем key
    """
    result_dict = {}
    for item in list:
        if objects: k_value = getattr(item, key)
        else: k_value = item[key]

        if not k_value in result_dict:
            result_dict[k_value] = []
        result_dict[k_value].append(item)

    return result_dict


def random_string(size=30, chars=string.ascii_letters+string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def url_with_querystring(path, **kwargs):
    for key, value in kwargs.iteritems():
        kwargs[key] = unicode(value).encode('utf-8')
    
    return path + u'?' + urllib.urlencode(kwargs)


#  Обработка Exception
def traceback_own(excpt, msg=None):
    if msg is None or not len(msg):
        msg = u''

    err_l = u'Error'
    if excpt.__class__.__name__ == 'KeyError':
        err_l = u'KeyError'

    exc_type, exc_value, exc_traceback = sys.exc_info()
    trace_msg = ''.join(traceback.format_tb(exc_traceback))

    print u'============={msg}================'.format(msg=msg.encode('utf-8'))
    print u'%s: %s' % (err_l, excpt)
    print u'============================='
    print u'Traceback:\n{trace_msg}'.format(trace_msg=trace_msg)
    print u'============================='


def isiterable(obj):
    try:
        iter(obj)
        return True
    except TypeError:
        return False

def dict_fetch_all(cursor):
    """Returns generator row"""

    desc = [col[0] for col in cursor.description]
    for row in cursor.fetchall():
        yield dict(zip(desc, row))


def dict_fetch_all_without_gen(cursor):
    """Returns all rows from a cursor as a dict"""

    desc = [col[0] for col in cursor.description]
    return [dict(zip(desc, row)) for row in cursor.fetchall()]

