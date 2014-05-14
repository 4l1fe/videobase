function select_p_a(){
    var p = $("p.file-upload")
    var a = p.children().select("a")
    var src = a.html()

    return {p:p,
            a:a,
            src:src}
}

// Helper function for csrf
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Global variables for storing crop coordinates
X=null;
Y=null;
X2=null;
Y2=null;
// Global variables for storing brightness contrast values.
BR = null;
CO = null;

function setCoords(c){
X=c.x;
Y=c.y;
X2=c.x2;
Y2=c.y2;

}
function init_resizing(){

    var a_p = select_p_a()

    var p = a_p.p
    var src = a_p.src
    p.append("<div id = 'slinks'><\div>")


    p.append("<div id ='to-resize'><img id = 'img-to-resize' src ='/static/"+src+"'></div>")

        $('#slinks').append('<a href= "http://images.google.com/searchbyimage?image_url='+ encodeURIComponent($('#img-to-resize')[0].src)+'"> Поискать картинку на Google<\a>')
    jQuery("#img-to-resize").Jcrop({
        onChange: setCoords,
        onSelect: setCoords
    });
}

function init_br_co(){

    var a_p = select_p_a();
    var p = a_p.p;
    var src = a_p.src;
    p.append("<div id='levels'></div>")
    var pl = $('#levels')
    pl.append("<img id = 'br-co' src ='/static/"+src+"'>")
    pl.append("<input id ='br_co_send' type='button' value = 'Save'>")
    pl.append("<br><div id='slider-brightness' >Яркость</div>")
    pl.append("<br><div id='slider-contrast' >Контраст</div>")

    Caman("#br-co",function(){

        var caman = this;

        $( "#slider-brightness" ).slider( {
            slide: function(event,ui) {
                caman.revert();
                BR = ui.value;
                caman.brightness(BR-50).render();
            },
            value:50});

        $( "#slider-contrast" ).slider( {
            slide: function(event,ui) {
                caman.revert();
                CO= ui.value;
                caman.contrast(CO-50).render();
            },
            value:50});

})

}

function add_buttons(){

    var p = select_p_a().p;
    p.append('<div id = "btns"></div>')
    var buttons = $('#btns')

    var res = buttons.append("<input id='resbut' style='width:100px' type='button' value = 'Режим обрезания'></input>")
    var br_co =buttons.append("<input id ='brcobut' style='width:100px' type='button' value = 'Изменение контрастаосвещенности'></input>")

    $("#to-resize").append("<input id ='bcrop' style='width:100px' type='button' value = 'Вырезать'></input>")

    $("#resbut").click(function(event,ui){
        if ($('#levels').length>0){
            $('#levels').hide();}
        $('#to-resize').show();
    })

    $("#brcobut").click(function(event,ui){
        if ($('#to-resize').length>0){
            $('#to-resize').hide();
        }
        if ($('#levels').length>0){
            $('#levels').show()}
    })

    $("#bcrop").click(function(event,ui){

        $.post('/api/image/resize/',{image:$('#img-to-resize')[0].src,
                                     x:X,
                                     y:Y,
                                     x2:X2,
                                     y2:Y2
                                    },function(){
                                  location.reload();
});
    })
    $("#br_co_send").click(function(event,ui){
        $.post('/api/image/brco/',{image:$('#img-to-resize')[0].src,
                                   br:BR,
                                   co:CO
                                  },
               function(){
                   location.reload();
   });
    })


}


function edit_mode_init(){
    $('#levels').hide()
}


function load_all(){

if ( $("p.file-upload").length >0){
    init_resizing();
    init_br_co();
    add_buttons();
    edit_mode_init();

}}

IS_IMAGE_EDITOR_SET = 0;

function predecision(){

    if ($('#id_etype').length >0){
        if ($('#id_type')[0].value =="POSTER"){
            load_all();
            IS_IMAGE_EDITOR_SET = 1;
            $('div.field-url').hide();
        }
        else{
            $('div.field-photo').hide();}

    }
    else{
        load_all();
        IS_IMAGE_EDITOR_SET = 1;
    }

    $('#id_type').change(function(event){

        if (event.target.value == "POSTER"){

            $('div.field-url').hide()
            $('div.field-photo').show()
            if (!IS_IMAGE_EDITOR_SET){
                load_all()
                IS_IMAGE_EDITOR_SET = 1;
            }}
        else{
            $('div.field-url').show()
            $('div.field-photo').hide()
        }
    })

}


jQuery(document).ready(predecision);




// Making our request csrf protection compatible

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
csrftoken =getCookie("csrftoken")
$.ajaxSetup({
    crossDomain: false, // obviates need for sameOrigin test
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type)) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});
