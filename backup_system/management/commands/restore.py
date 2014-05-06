# coding: utf-8
from django.core.management import BaseCommand

from backup_system.constants import APP_BACKUP_FILENAME_TEMPLATE

from optparse import make_option
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
        path = settings.BACKUP_PATH
        db_name = settings.DATABASES['default']['NAME']
        db_user = settings.DATABASES['default']['USER']
        db_host = settings.DATABASES['default']['HOST']
        db_port = settings.DATABASES['default']['PORT']
        filename = options['filename']

        if filename is None:
            times = map(lambda f: f.split('_')[2].split('.')[0], os.listdir(path))
            s_times = sorted(times, key=lambda t: time.strptime(t, "%Y-%m-%d-%H-%M"))
            filename = APP_BACKUP_FILENAME_TEMPLATE.format(db_name=db_name,
                                                           time=s_times[-1])

        file_path = os.path.join(path, filename)
        logger.info("End: processed params to restore backup")
        if not os.path.exists(file_path):
            logger.error("File doesn't exists: {0}".format(file_path))
            return None
        logger.info("Start: restore DATABASE: {0} from {1}".format(db_name, file_path))
        try:
            restore_command = "pg_restore --dbname={name} --username={user} --host={host} --port={port} -F c {filename}".\
                format(filename=file_path, name=db_name, user=db_user,
                       host=db_host, port=db_port)
            os.popen(restore_command)
            logger.info("End: restore DATABASE: {0} from {1}".format(db_name, file_path))
        except Exception as e:
            logger.error("""End: restore DATABASE: {0} from {1}
                            error: {2}""".format(db_name, file_path, e))
        return None

