conf =
  static_url: "/static/"

conf.images_url = conf.static_url + '/img/'
conf.tpl_url = conf.static_url + '/tpl/'
conf.api_url = "/api/v1/"
conf.noposter_url = conf.images_url +  "noposter.png"
conf.noavatar_url = conf.images_url + "noavatar.png"
conf.noperson_url = conf.images_url + "noperson.jpg"
conf.filter_delay = 1000

window.mi_conf = conf
