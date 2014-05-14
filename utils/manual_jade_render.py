import os
import sys
from pprint import pprint as pp
from bs4 import BeautifulSoup as BS

sys.path.append(os.path.abspath('../..'))
os.environ["DJANGO_SETTINGS_MODULE"] = "videobase.settings"

from apps.films.models import Persons, PersonsFilms
from apps.films.api.serializers import vbPerson, vbFilm
from noderender import render_page

os.chdir('..')

p = Persons.objects.get(pk=875)
vbp = vbPerson(p, extend=True)
pfs = PersonsFilms.objects.filter(person=p)[:12]
vbf = vbFilm([pf.film for pf in pfs], many=True)

res = render_page('person', {'person': vbp.data, 'filmography': vbf.data})
soup = BS(res)
print(soup.prettify())