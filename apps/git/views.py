# coding: utf-8
import os
import json
from git import Repo

from django.http import HttpResponse

from videobase.settings import BASE_DIR


def info(request):
    path = os.path.abspath(os.path.join(BASE_DIR, '.git'))
    repo = Repo(path)
    return HttpResponse(json.dumps({
        'branch': repo.active_branch,
        'commit': repo.commits(repo.active_branch)[0].id,
    }))
