# coding: utf-8
from django.db import connection
from django.contrib.admin.models import LogEntry

class LogentrySummary:
    def __init__(self, **args):
        self.args = args

    def summary(self):
        sql = """
          SELECT users.id,
                 (users.firstname || users.lastname) as "username",
	         django_admin_log.action_flag,
	         django_admin_log.content_type_id,
	         count(*)
          FROM django_admin_log
               INNER JOIN users ON users.id = django_admin_log.id
          GROUP BY users.id,
	           users.firstname,
                   users.lastname,
	           django_admin_log.action_flag,
	           django_admin_log.content_type_id;

        """
        try:
            cursor = connection.cursor()

            #cursor.execute("UPDATE bar SET foo = 1 WHERE baz = %s", [self.baz])
            cursor.execute(sql)

            return [
                dict(zip(['user_id', 'user_name', 'action', 'type', 'count'], row))
                for row in cursor.fetchall()
            ]
        finally:
            cursor.close()
