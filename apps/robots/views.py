# coding: utf-8
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def schedule_interface(request):


    if request.method =="GET":

        return HttpResponse("""
        <html>
        <head>
        <script src="http://code.jquery.com/jquery-1.9.1.js" type="text/javascript"></script>
        </head>
        <body>
        </body>
        <script>

        function setInitial(){

        }

        </script>

        <div>Периодичность запуска робота для кинопоиска<input type='text' id = 'kinopoisk'></div>
        <div>Периодичность запуска робота для IMDB<input type='text' id = 'imdb'></div>
        </body>
        </html>
        """)

def schedule_api(request):

    return HttpResponse('''Not implemented''')
    
