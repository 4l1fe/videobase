# coding: utf-8
from django.core.management import BaseCommand

from backup_system.constants import APP_BACKUP_FILENAME_TEMPLATE

from optparse import make_option
import subprocess
import logging
import os
import time

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


class Command(BaseCommand):

    help = u'Backup database'
    option_list = BaseCommand.option_list + (
    )

    def handle(self, *args, **options):
        logger.info("Start: processed params to backup")
        settings_module = options['settings']
        if settings_module is None:
            settings_module = 'videobase.settings'
        settings = __import__(settings_module).settings
        try:
            path = settings.BACKUP_PATH
            db_name = settings.DATABASES['default']['NAME']
            db_user = settings.DATABASES['default']['USER']
            db_host = settings.DATABASES['default']['HOST']
            db_port = settings.DATABASES['default']['PORT']
        except Exception as e:
            logger.error("End: Backup DATABASE with error: {0}".format(e))
            return None
        try:
            os.makedirs(path)
        except os.error:
            logger.warning("Path {0} exists".format(os.path.abspath(path)))
        except Exception as e:
            pass
        logger.info("End: Processed params to backup")
        logger.info("Start: backup for DATABASE: {0}".format(db_name))
        try:
            backup_file = APP_BACKUP_FILENAME_TEMPLATE.format(db_name=db_name,
                                                              time=str(time.strftime("%Y-%m-%d-%H-%M")))
            command = "pg_dump {name} --username {user} --host={host} --port={port} -F c > {filename} ".\
                format(name=db_name, user=db_user, host=db_host,
                       port=db_port, filename=os.path.join(path, backup_file))
            p = subprocess.Popen(command, shell=True).wait()
            logger.info("End: Backup for DATABASE: {0}".format(db_name))
        except Exception as e:
            logger.error("""End: Backup for DATABASE:{0}
                   error: {1}""".format(db_name, e))
        return None
