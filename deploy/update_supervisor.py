#!/bin/python
SUPERVISOR_FILE = '/etc/supervisor/conf.d/gunicorn.conf'
import os
import re

with open(SUPERVISOR_FILE) as  cf:
    data = cf.read()

modified = re.sub('directory=.+','directory={}'.format(os.path.abspath('')),data)
with open(SUPERVISOR_FILE,'w') as cf:
    data = cf.write(modified)

