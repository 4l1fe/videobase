from data.sitemap import refresh
from videobase.celery import app


@app.task(name='refresh_sitemap')
def refresh_sitemap_task():

    refresh()

