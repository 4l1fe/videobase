from data.sitemap import refresh
from videobase.celery import app
from apps.films.management.commands.consolidate_rating import Command

@app.task(name='refresh_sitemap')
def refresh_sitemap_task():

    refresh()


@app.task(name='consolidate_rating')
def consolidate_rating_task():

    c = Command()
    c.handle()

