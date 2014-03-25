# coding: utf-8
from django.db import connection
from django.contrib.admin.models import LogEntry, DELETION, ADDITION, CHANGE

class LogentrySummary:
    def __init__(self, **args):
        self.start_at = args['period']['start_at']
        self.end_at = args['period']['end_at']
        pass

    def summary(self):
        sql = """
        SELECT users.id,
                 (users.firstname || users.lastname) as "username",
	         django_admin_log.action_flag,
	         django_content_type.name,
	         count(*)
          FROM django_admin_log
               INNER JOIN users ON users.id = django_admin_log.user_id
               INNER JOIN django_content_type ON django_content_type.id = django_admin_log.content_type_id
          WHERE django_admin_log.action_time between %s AND %s
          GROUP BY users.id,
	           users.firstname,
                   users.lastname,
	           django_admin_log.action_flag,
	           django_content_type.name;
        """
        try:
            cursor = connection.cursor()
            cursor.execute(sql, [self.start_at, self.end_at])
            return [self.__prepare_data( row) for row in cursor.fetchall()]

        finally:
            cursor.close()

    def __action_description(self, action_flag):
        action_names = {
            ADDITION: 'Addition',
            DELETION: 'Deletion',
            CHANGE: 'Change',
        }
        return action_names[action_flag]

    def __prepare_data(self, row):
        return dict(zip(['user_id', 'user_name', 'action', 'type', 'count'],
                        [row[0],
                        row[1],
                        self.__action_description(row[2]),
                        row[3],
                         row[4]]))
