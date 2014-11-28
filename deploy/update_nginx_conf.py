#!/bin/python

import os
import re

with open('configs_from_repo/nginx_local.conf') as  cf:
    data = cf.read()

modified = re.sub('set[ ][$]videobase_root.','set $videobase_root {}'.format(os.path.abspath('.')),data)
with open('vsevi.conf','w') as cf:
    data = cf.write(modified)
