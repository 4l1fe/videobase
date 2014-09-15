

function add_name_links(){
    //var r = new RegExp("\[[0-9]+\][ ](.+)");
    //var ht = $('div.field-film').find('strong').html()
    var name =$("#id_name")[0].value //ht.match(r)[1];

    console.log(name)
    $('div.field-name').append('<br><div><a href= "http://google.com/search?q='+encodeURIComponent(name)+'">Поискать на Google</a></div>')

    $('div.field-name').append('<div><a href= "http://yandex.ru/yandsearch?text='+encodeURIComponent(name)+'">Поискать на Яндексе</a></div>')
    var id_imdb_id =$("#id_imdb_id")[0].value;
    $('div.field-imdb_id').append("<a href = 'http://www.imdb.com/title/tt0"+id_imdb_id +"/'> Страница фильма на IMDB</a>")

    var id_kinopoisk_id =$("#id_kinopoisk_id")[0].value;
    $('div.field-kinopoisk_id').append("<a href = 'http://www.kinopoisk.ru/film/"+id_kinopoisk_id +"/'> Страница фильма на Кинопоиске</a>")


}


jQuery(document).ready(add_name_links);
