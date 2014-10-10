window.mi_templates = {"cast-thumb":function template(locals) {
var buf = [];
var jade_mixins = {};
var jade_interp;
;var locals_for_with = (locals || {});(function (static_url, img_url, noavatar_url, nophoto_url, noposter_url, js_url, css_url, IN_PRODUCTION, location_names, quality_texts, months, date_now, Date, undefined, parseInt, Math, res, min, start_date, generic_title, title, title_orig, pg_rating, poster_url, url, watching_users_count, curr_date, end_date, start_date_class, is_online, start_in_date, has_free, min_price, price_loc, btn_cls, price_loc_cnt, i, obj, url_loc, url_btn, btn_text, title_alt, time_to_wait_str, start_in_minutes, archive_date_text, text, cast) {
static_url = "/static/"
img_url = static_url + "img/"
noavatar_url = img_url + "noavatar.png"
nophoto_url = img_url + "nophoto.png"
noposter_url = img_url + "noposter.png"
js_url = static_url + "js/"
css_url = static_url + "css/"
IN_PRODUCTION = true
location_names = {"drugoekino": "Другое Кино", "youtubemoviesru": "Youtube Movies", "ivi": "IVI.ru", "nowru": "Now.ru", "megogo": "Megogo", "tvigle": "TVigle", "zoomby": "Zoomby.ru", playfamily: "PlayFamily.ru", "olltv": "Oll.tv", amediateka: "Amediateka", molodejj: "Molodejj.tv", streamru: "Stream.ru", tvzavr: "TVzavr.ru", viaplay: "Viaplay.ru", zabavaru: "Zabava.ru", playgoogle: "Play Google", itunes: "Apple Itunes", ayyo: "Ayyo.ru", mosfilm: "Cinema.mosfilm.ru", "default": "Неизвестно"}
quality_texts = {"norm": "Отличное", "hd": "Хорошее", "fhd": "Full<strong>HD</strong>", "default": "Хорошее"}
months = ["января", "февраля", "марта", "апреля", "мая", "июня", "июля", "августа", "сентября", "октября", "ноября", "декабря"]
date_now = new Date()
function how_long_str(str, level) {
try {
return how_long(new Date(str), level);
} catch (e) {
return "";
}
}
function how_long(dt, level) {
var months, years, days, res;
years = date_now.getFullYear() - dt.getFullYear();
months = date_now.getMonth() - dt.getMonth();
days = date_now.getDate() - dt.getDate();
if (days < 0) {
months--;
days = date_now.getDate() + new Date(dt.getFullYear(), dt.getMonth() + 1, 0).getDate() - dt.getDate()
}
res = "";
if (months < 0) {
years--;
months+= 12;
}
if (level == undefined) level = 0
if (years > 0 || level == 0) res = years + cardinal(years, " год", " года", " лет");
if (level > 0) {
if (months > 0 || level == 1) res+= (res?" ":"") + months + cardinal(months, " месяц", " месяца", " месяцев")
if (level > 1) {
if (days > 0 || level == 2) res+= (res?" ":"") + days + cardinal(days, " день", " дня", " дней");
}
}
return res;
}
function string_to_date(str) {
//yyyy-mm-dd hh:mm:ss
var ar1, ar2, ar3;
ar1 = str.split(" ")
ar2 = ar1[0].split("-")
ar3 = ar1[1]?ar1[1].split(":"):[0,0,0]
return new Date(ar2[0],parseInt(ar2[1]) - 1,ar2[2],ar3[0],ar3[1],ar3[2])
}
function cardinal(val, form1, form2, form3) {
var d10;
if (val > 4 && val < 21) return form3;
d10 = val % 10;
if (d10 == 0 || d10 > 4) return form3;
if (d10 == 1) return form1;
return form2;
}
function duration_text(min) {
var ho, mi;
ho = Math.floor(min / 60); mi = min - ho*60;
res = ho?ho + cardinal(ho, " час", " часа", " часов"):"";
if (mi) res+= (res?" ":"") + mi + cardinal(mi, " минута", " минуты", " минут")
return res || "0 минут";
}
function date_text_str(str) {
try {
return date_text(new Date(str));
} catch (e) {
return str;
}
}
function date_text(dt) {
return dt.getDate() + " " + months[dt.getMonth()] + " " + dt.getFullYear() + " г.";
}
function time_text_str(str) {
try {
return time_text(new Date(str));
} catch (e) {
return str;
}
}
function time_text(dt) {
var diff, curday, curtime, ho;
curtime = dt.getTime();
diff = (date_now.getTime() - curtime) / 1000;
if (diff < 60) return "сейчас";
if (diff < 3600) {
min = Math.floor(diff / 60)
return min + cardinal(min, " минуту", " минуты", " минут") + " назад"
}
curday = Math.floor(date_now.getTime() / 86400) * 86400;
if (curday < curtime) {
ho = Math.floor(diff / 3600);
if (ho <= 6) {
return ho + cardinal(ho, " час", " часа", " часов") + " назад";
} else return "сегодня";
}
if ((curday - 86400) < curtime) return "вчера";
if (dt.getFullYear() == date_now.getFullYear()) return dt.getDate() + " " + months[dt.getMonth()];
return dt.getDate() + " " + months[dt.getMonth()] + " " + dt.getFullYear();
}















































































































































































jade_mixins["cast_thumb"] = function(item){
var block = (this && this.block), attributes = (this && this.attributes) || {};
buf.push("<div data-mi-id=\"id\"" + (jade.attr("data-mi-val", item.id, true, false)) + " class=\"col-md-3 col-sm-4 col-xs-6 cast-thumb\">");
start_date = item.start ? new Date(item.start*1000) : null
generic_title = item.generic_title //Тэг/ обобщенное название
title = item.title //Конкретное название
title_orig = item.title_orig
pg_rating = item.pg_rating
poster_url = item.poster
url = "/casts/" + item.id + "/"
watching_users_count = item.watching_users_count
curr_date = new Date()
item.start_in = Math.floor(  ( start_date.getTime() - curr_date.getTime() )/1000  )
item.duration = 1000
end_date = new Date(start_date)
end_date.setMinutes(start_date.getMinutes() + item.duration)
start_date_class = is_online ? "label-success" : "label-primary"
start_in_date = new Date(item.start_in*1000)
has_free = false
min_price = false
price_loc = ""
btn_cls = ""
price_loc_cnt = 0
if ( start_date < curr_date ) {
if( item.locations && item.locations.length ) {
{
for (i = 0; i < item.locations.length; i++) {
obj = item.locations[i];
if (obj.price_type == 0) {
has_free = true;
} else {
price_loc_cnt++;
if (min_price === false || min_price > obj.price) {
min_price = obj.price;
price_loc = obj.id
}
}
}
}
}
if (min_price) {
min_price = Math.floor(min_price)
}
url_loc = price_loc?(url+"#" + price_loc):""
url_btn = url
if (min_price && !has_free) {
btn_cls = "btn-price"
btn_text = "Смотреть<br><i>" + (price_loc_cnt > 1?"от ":"") + min_price + " р. без рекламы</i>"
url_btn = url_loc
} else {
btn_cls = "btn-free"
btn_text = "Смотреть<br/>бесплатно"
url_btn = url + "#player"
}
} else {
btn_cls = "btn-subscribe"
btn_text = "Подписаться"
}
buf.push("<a" + (jade.attr("href", url, true, false)) + " title=\"\" data-mi-athref=\"id\" class=\"poster-place\">");
title_alt = ( generic_title ? generic_title + '. ' : '' ) + title
if (title_orig && title_orig != title_orig) title_alt += " (" + title_orig + ")"
buf.push("<img" + (jade.attr("src", poster_url || noposter_url, true, false)) + " data-mi-atsrc=\"poster\"" + (jade.attr("data-mi-default", noposter_url, true, false)) + " data-mi-id=\"poster\"" + (jade.attr("title", title_alt, true, false)) + (jade.attr("alt", title_alt, true, false)) + " data-mi-attitle=\"title_alt\" data-mi-atalt=\"title_alt\" class=\"img-poster\"/></a><img" + (jade.attr("src", img_url + 'shd-small.png', true, false)) + " alt=\"\"/><div class=\"cast-item-def\"><div class=\"cast-item-status\">");
time_to_wait_str = ''
if ( curr_date < start_date ) {
if( item.start_in < 86400 ) {
start_in_minutes = Math.floor(item.start_in / 60)
time_to_wait_str = ( start_in_minutes < 60 ? 'примерно ' : '' ) + 'через ' + duration_text( start_in_minutes )
} else {
time_to_wait_str += start_date.getDate() + ' ' +  months[start_date.getMonth()]
time_to_wait_str += ' в ' + start_date.getHours() + ':' + ( start_date.getMinutes() < 10 ? '0' : '' ) + start_date.getMinutes()
}
{
buf.push("<div class=\"label label-primary\">" + (jade.escape(null == (jade_interp = time_to_wait_str) ? "" : jade_interp)) + "</div>");
}
} else if( curr_date < end_date ) {
{
if( watching_users_count !== null && watching_users_count !== undefined )
{
buf.push("<div class=\"fright cast-watching-users-count\">смотрят:\n " + (jade.escape(null == (jade_interp = watching_users_count) ? "" : jade_interp)) + "</div>");
}
buf.push("<div class=\"label label-success\">online</div>");
}
} else {
{
archive_date_text = start_date.getDate() + ' ' + months[start_date.getMonth()]
if (start_date.getFullYear() !== curr_date.getFullYear() ) {
archive_date_text += " " + start_date.getFullYear()
}
buf.push("<div class=\"fright cast-archive-date\">" + (jade.escape(null == (jade_interp = archive_date_text) ? "" : jade_interp)) + "</div><div class=\"label label-primary\">Архив</div>");
}
}
buf.push("</div><div class=\"cast-item-header\"><a" + (jade.attr("href", url, true, false)) + " title=\"\" data-mi-athref=\"id\"><span class=\"cast-item-title\">" + (jade.escape(null == (jade_interp = title) ? "" : jade_interp)) + "</span><span data-mi-name=\"pg_rating\" data-mi-id=\"pg_rating\"" + (jade.attr("data-mi-val", pg_rating, true, false)) + " class=\"cast-item-pg-rating\"> (" + (jade.escape(null == (jade_interp = pg_rating) ? "" : jade_interp)) + ")</span></a></div><div data-mi-id=\"btn\"" + (jade.cls(['btn-def','block',btn_cls], [null,null,true])) + "><a" + (jade.attr("href", url_btn, true, false)) + " title=\"\" data-mi-id=\"btn_text\" data-mi-athref=\"id\">" + (null == (jade_interp = btn_text) ? "" : jade_interp) + "</a></div><p data-mi-id=\"btn_price\"" + (jade.cls([min_price && has_free?'':'display-none'], [true])) + ">или<a" + (jade.attr("href", url_loc, true, false)) + " title=\"\" data-mi-athref=\"id\">");
text = " " + (price_loc_cnt > 1?"от ":"") + min_price + " р. без рекламы"
buf.push("<span data-mi-id=\"price\">" + (jade.escape(null == (jade_interp = text) ? "" : jade_interp)) + "</span></a></p></div></div>");
};
















jade_mixins["cast_thumb"](cast);}.call(this,"static_url" in locals_for_with?locals_for_with.static_url:typeof static_url!=="undefined"?static_url:undefined,"img_url" in locals_for_with?locals_for_with.img_url:typeof img_url!=="undefined"?img_url:undefined,"noavatar_url" in locals_for_with?locals_for_with.noavatar_url:typeof noavatar_url!=="undefined"?noavatar_url:undefined,"nophoto_url" in locals_for_with?locals_for_with.nophoto_url:typeof nophoto_url!=="undefined"?nophoto_url:undefined,"noposter_url" in locals_for_with?locals_for_with.noposter_url:typeof noposter_url!=="undefined"?noposter_url:undefined,"js_url" in locals_for_with?locals_for_with.js_url:typeof js_url!=="undefined"?js_url:undefined,"css_url" in locals_for_with?locals_for_with.css_url:typeof css_url!=="undefined"?css_url:undefined,"IN_PRODUCTION" in locals_for_with?locals_for_with.IN_PRODUCTION:typeof IN_PRODUCTION!=="undefined"?IN_PRODUCTION:undefined,"location_names" in locals_for_with?locals_for_with.location_names:typeof location_names!=="undefined"?location_names:undefined,"quality_texts" in locals_for_with?locals_for_with.quality_texts:typeof quality_texts!=="undefined"?quality_texts:undefined,"months" in locals_for_with?locals_for_with.months:typeof months!=="undefined"?months:undefined,"date_now" in locals_for_with?locals_for_with.date_now:typeof date_now!=="undefined"?date_now:undefined,"Date" in locals_for_with?locals_for_with.Date:typeof Date!=="undefined"?Date:undefined,"undefined" in locals_for_with?locals_for_with.undefined:typeof undefined!=="undefined"?undefined:undefined,"parseInt" in locals_for_with?locals_for_with.parseInt:typeof parseInt!=="undefined"?parseInt:undefined,"Math" in locals_for_with?locals_for_with.Math:typeof Math!=="undefined"?Math:undefined,"res" in locals_for_with?locals_for_with.res:typeof res!=="undefined"?res:undefined,"min" in locals_for_with?locals_for_with.min:typeof min!=="undefined"?min:undefined,"start_date" in locals_for_with?locals_for_with.start_date:typeof start_date!=="undefined"?start_date:undefined,"generic_title" in locals_for_with?locals_for_with.generic_title:typeof generic_title!=="undefined"?generic_title:undefined,"title" in locals_for_with?locals_for_with.title:typeof title!=="undefined"?title:undefined,"title_orig" in locals_for_with?locals_for_with.title_orig:typeof title_orig!=="undefined"?title_orig:undefined,"pg_rating" in locals_for_with?locals_for_with.pg_rating:typeof pg_rating!=="undefined"?pg_rating:undefined,"poster_url" in locals_for_with?locals_for_with.poster_url:typeof poster_url!=="undefined"?poster_url:undefined,"url" in locals_for_with?locals_for_with.url:typeof url!=="undefined"?url:undefined,"watching_users_count" in locals_for_with?locals_for_with.watching_users_count:typeof watching_users_count!=="undefined"?watching_users_count:undefined,"curr_date" in locals_for_with?locals_for_with.curr_date:typeof curr_date!=="undefined"?curr_date:undefined,"end_date" in locals_for_with?locals_for_with.end_date:typeof end_date!=="undefined"?end_date:undefined,"start_date_class" in locals_for_with?locals_for_with.start_date_class:typeof start_date_class!=="undefined"?start_date_class:undefined,"is_online" in locals_for_with?locals_for_with.is_online:typeof is_online!=="undefined"?is_online:undefined,"start_in_date" in locals_for_with?locals_for_with.start_in_date:typeof start_in_date!=="undefined"?start_in_date:undefined,"has_free" in locals_for_with?locals_for_with.has_free:typeof has_free!=="undefined"?has_free:undefined,"min_price" in locals_for_with?locals_for_with.min_price:typeof min_price!=="undefined"?min_price:undefined,"price_loc" in locals_for_with?locals_for_with.price_loc:typeof price_loc!=="undefined"?price_loc:undefined,"btn_cls" in locals_for_with?locals_for_with.btn_cls:typeof btn_cls!=="undefined"?btn_cls:undefined,"price_loc_cnt" in locals_for_with?locals_for_with.price_loc_cnt:typeof price_loc_cnt!=="undefined"?price_loc_cnt:undefined,"i" in locals_for_with?locals_for_with.i:typeof i!=="undefined"?i:undefined,"obj" in locals_for_with?locals_for_with.obj:typeof obj!=="undefined"?obj:undefined,"url_loc" in locals_for_with?locals_for_with.url_loc:typeof url_loc!=="undefined"?url_loc:undefined,"url_btn" in locals_for_with?locals_for_with.url_btn:typeof url_btn!=="undefined"?url_btn:undefined,"btn_text" in locals_for_with?locals_for_with.btn_text:typeof btn_text!=="undefined"?btn_text:undefined,"title_alt" in locals_for_with?locals_for_with.title_alt:typeof title_alt!=="undefined"?title_alt:undefined,"time_to_wait_str" in locals_for_with?locals_for_with.time_to_wait_str:typeof time_to_wait_str!=="undefined"?time_to_wait_str:undefined,"start_in_minutes" in locals_for_with?locals_for_with.start_in_minutes:typeof start_in_minutes!=="undefined"?start_in_minutes:undefined,"archive_date_text" in locals_for_with?locals_for_with.archive_date_text:typeof archive_date_text!=="undefined"?archive_date_text:undefined,"text" in locals_for_with?locals_for_with.text:typeof text!=="undefined"?text:undefined,"cast" in locals_for_with?locals_for_with.cast:typeof cast!=="undefined"?cast:undefined));;return buf.join("");
}};