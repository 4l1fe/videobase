

function add_name_links(){
    //var r = new RegExp("\[[0-9]+\][ ](.+)");
    //var ht = $('div.field-film').find('strong').html()
    var name =$("#id_name")[0].value //ht.match(r)[1];

    console.log(name)
    $('div.field-name').append('<br><div><a href= "http://google.com/search?q='+encodeURIComponent(name)+'">Поискать на Google</a></div>')

    $('div.field-name').append('<div><a href= "http://yandex.ru/yandsearch?text='+encodeURIComponent(name)+'">Поискать на Яндексе</a></div>')

}


jQuery(document).ready(add_name_links);
