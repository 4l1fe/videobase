# coding: utf-8
import os
import re
import time
import logging
import subprocess
from optparse import make_option

from django.core.management import BaseCommand

from backup_system.constants import APP_BACKUP_FILENAME_TEMPLATE


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


class Command(BaseCommand):

    help = u'Restore Database from backup'
    option_list = BaseCommand.option_list + (
        make_option(u'-f', u'--filename', action=u'store', type=u'string',
                    dest=u'filename', help=u'Name of backup file to restore'),
    )

    def handle(self, *args, **options):
        logger.info("Start: processed params to restore backup")
        settings_module = options['settings']

        if settings_module is None:
            settings_module = 'videobase.settings'

        settings = __import__(settings_module).settings
        try:
            path = settings.BACKUP_PATH
            if not os.path.exists(path):
                raise Exception("{0} not exists".format(path))
            db_name = settings.DATABASES['default']['NAME']
            db_user = settings.DATABASES['default']['USER']
            db_host = settings.DATABASES['default']['HOST']
            db_port = settings.DATABASES['default']['PORT']
            db_pass = settings.DATABASES['default']['PASSWORD']
            filename = options['filename']
        except Exception as e:
            logger.error("End: restore DATABASE with error: {0}".format(e))
            return None

        if filename is None:
            search_string = "{0}_dump_".format(db_name) + "\d{4}(-\d{2}){4}.sql"
            files = filter(lambda f: True if re.match(search_string, f) else False, os.listdir(path))
            times = map(lambda f: f.split('_')[2].split('.')[0], files)
            s_times = sorted(times, key=lambda t: time.strptime(t, "%Y-%m-%d-%H-%M"))
            filename = APP_BACKUP_FILENAME_TEMPLATE.format(db_name=db_name, time=s_times[-1])

        file_path = os.path.join(path, filename)
        logger.info("End: processed params to restore backup")
        if not os.path.exists(file_path):
            logger.error("File doesn't exists: {0}".format(file_path))
            return None

        try:
            logger.info("Start: drop and create schema 'public' in DATABASE: {}".format(db_name))
            command = "PGPASSWORD={passwd} psql --username={user} --dbname={name} --host={host} --port={port} --command='DROP SCHEMA IF EXISTS public CASCADE;'".\
                format(passwd=db_pass, name=db_name, user=db_user, host=db_host, port=db_port)

            p = subprocess.Popen(command, shell=True).wait()
            logger.info("Delete schema.")
            command = "PGPASSWORD={passwd} psql --username={user} --dbname={name} --host={host} --port={port} --command='CREATE SCHEMA public AUTHORIZATION {user};'".\
                format(passwd=db_pass, name=db_name, user=db_user, host=db_host, port=db_port)

            p = subprocess.Popen(command, shell=True).wait()
            logger.info("Create schema.")
            logger.info("End: drop and create schema 'public' in DATABASE: {}".format(db_name))
        except Exception as e:
            logger.error("End: drop and create schema 'public' in DATABASE: {1} error: {2}".format(db_name, e))
            return None

        logger.info("Start: restore DATABASE: {0} from {1}".format(db_name, file_path))
        try:
            command = "PGPASSWORD={passwd} pg_restore --dbname={name} --username={user} --host={host} --port={port} -F c {filename}".\
                format(passwd=db_pass, filename=file_path, name=db_name, user=db_user,
                       host=db_host, port=db_port)

            p = subprocess.Popen(command, shell=True).wait()
            logger.info("End: restore DATABASE: {0} from {1}".format(db_name, file_path))
        except Exception as e:
            logger.error("End: restore DATABASE: {0} from {1} error: {2}".format(db_name, file_path, e))

        return None

