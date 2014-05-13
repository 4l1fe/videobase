'use strict'

window.mi_app = undefined

error = (txt, type = "norm") ->
  if type == "crit"
    throw new Error "CRITICAL ERROR: " + txt
  else
    console.log "ERROR: " + txt

check_app_is_init = (c) ->
  if !window.mi_app
    error "App is not init", "crit"
  else
    c._app = window.mi_app

state_toggle = (new_state, cur_state, deflt)->
  if new_state == undefined
    if cur_state == undefined
      if deflt != undefined
        return deflt
      else
        return 1
    else if cur_state
      return 0
    else
      return 1
  else
    new_state?1:0

locations_type_text =
  ivi: "IVI.ru"
  nowru: "NOW.ru"
  zoomby: "Zoomby.ru"
  megogo: "Megogo.net"
  tvigle: "Tvigle.ru"
  playfamily: "PlayFamily.ru"
  amediateka: "Amediateka"
  molodejj: "Molodejj.tv"
  stream: "Stream.ru"
  tvzavr: "TVzavr.ru"
  viaplay: "Viaplay.ru"
  zabava: "Zabava.ru"
  playgoogle: "Play Google"
  itunes: "Apple Itunes"
  ayyo: "Ayyo.ru"
  mosfilm: "Cinema.mosfilm.ru"
  olltv: "oll.tv"

location_type_to_text = (type) ->
  locations_type_text[type.toLowerCase()] || type

class Player
  constructor: (@place, opts = {}) ->
    @current = undefined

  load: (loc) ->
    if @current != undefined
      @clear()
    html = undefined
    type = loc.type
    value = loc.value
    ratio = 1
    width = @place.width()
    if type == "ivi"
      value = loc.url_view.substr(24)
      value = value.substr(0, value.indexOf("#"))
      ratio = 640 / 360
      height = parseInt(width / ratio)
      html = '<object id="DigitalaccessVideoPlayer" classid="clsid:d27cdb6e-ae6d-11cf-96b8-444553540000" width="100%" height="100%" type="application/x-shockwave-flash" data="http://www.ivi.ru/video/player?siteId=s138&amp;_isB2C=1&amp;autoStart=1&amp;videoId=' + value + '&amp;allowSeriesPlaylist=1&amp;disableiviredirect=0&amp;share_embed=0"><param name="movie" value="http://www.ivi.ru/video/player?siteId=s138&amp;_isB2C=1&amp;autoStart=1&amp;videoId=' + value + '&amp;allowSeriesPlaylist=1&amp;disableiviredirect=0&amp;share_embed=0"><param name="allowScriptAccess" value="always"><param name="allowFullScreen" value="true"><param name="bgcolor" value="#000000"><param name="wmode" value="opaque"><embed quality="high" allowscriptaccess="always" allowfullscreen="true" wmode="opaque" width="100%" height="100%" type="application/x-shockwave-flash" src="http://www.ivi.ru/video/player?siteId=s138&amp;_isB2C=1&amp;autoStart=1&amp;videoId=' + value + '&amp;allowSeriesPlaylist=1&amp;disableiviredirect=0&amp;share_embed=0"></object>'
    else if type == "nowru"
      arr = loc.url_view.split("/")
      value = arr[arr.length - 1]
      html = '<iframe name="now1023318" src="http://www.now.ru/embed/frame/' + value + '" scrolling="no" frameborder="no" height="100%" width="100%"></iframe>'
      ratio = 860 / 480
    else if type == "tvigle"
      arr = loc.url_view.split("=")
      value = arr[arr.length - 1]
      # f_value = "http://photo.tvigle.ru/resource/rf/swf/" + value.substr(0,2) + "/" + value.substr(2,2) + "/" + value.substr(4,2) + "/" + value.substr(6) + ".swf"
      ratio = 720 / 539
      height = Math.round(width / ratio)
      html = '<object type="application/x-shockwave-flash" data="http://tvigle.ru/swf/tvigle_v12.swf?ver=3.597999999999975" width="1080" height="608" id="plr" style="visibility: visible; width: 1080px; height: 607.5px;"><param name="allowScriptAccess" value="always"><param name="bgcolor" value="#000000"><param name="quality" value="high"><param name="scale" value="noscale"><param name="allowFullScreen" value="true"><param name="wmode" value="opaque"><param name="flashvars" value="ref=1&amp;obj=' + value + '&amp;cnl=692685&amp;sid_name=&amp;user_sid=&amp;own=0&amp;w=1080&amp;h=608&amp;ap=1&amp;afbr=1&amp;region=RU&amp;skin=&amp;d=tvigle.ru"></object>'
      # html = '<object id="v' + value + '" classid="clsid:d27cdb6e-ae6d-11cf-96b8-444553540000" codebase="http://download.macromedia.com/pub/shockwave/cabs/flash/swflash.cab#version=9,0,0,0" width="100%" height="100%" align="middle"><param name="allowFullScreen" value="true"></param><param name="allowscriptaccess" value="always"></param><param name="movie" value="' + f_value + '"></param><embed src="' + f_value + '" width="100%" height="100%"  allowfullscreen="true" allowscriptaccess="always" type="application/x-shockwave-flash" pluginspage="http://www.macromedia.com/go/getflashplayer" /></object>'
    else if type == "streamru"
      html = ""
    else if type == "zoomby"
      value = 184209
      html = '<iframe src="http://www.zoomby.ru/v/' + value + '" width="100%" height="100%"></iframe>'
      ratio = 640 / 360

    if html != undefined
      @current = loc
      @place.height(@place.width() / ratio).html(html)

  clear: ->
    @place.addClass("player-empty")
    @place.empty().height("auto")
    @current = undefined

# a basic Page class
class Page
  constructor: () ->
    check_app_is_init(@)
    @_e = {}
    @_visible = false

  show: ->
    @_visible = true

  hide: ->
    @_visible = false

  isVisible: ->
    return @_visible

  user_is_auth: ->
    return @_app.user_is_auth()

class Item
  constructor: (opts = {}, callback = undefined) ->
    check_app_is_init(@)
    if (!@_name)
      error "It's wrong to use parent class", "crit"
    @vals = {}
    @defaults = {}
    @elements = {}
    @e_attrs = {}
    @e_vals = {}

    $.extend @defaults, opts.defaults if opts.defaults
    if opts.place == undefined
      @_place = $('<span class="preload-' + @_name + '"></span>')
      if opts.parent
        @_place.appendTo(opts.parent)
      @_app.get_tpl(
        @_name
        (tpl_obj) =>
          if tpl_obj
            old_place = @_place
            @_place = tpl_obj.clone()
            @set_elements()
            @set_vals opts.vals, opts.do_not_set if opts.vals
            @_place.insertAfter(old_place)
            old_place.remove()
            callback @ if callback
          else
            error 'Unable to load template for object "' + @_name + '"'
      )
    else
      @_place = opts.place
      @set_elements()
      @set_vals opts.vals, opts.do_not_set if opts.vals
      callback @ if callback

  place: ->
    @_place

  parse_element: ($this) ->
    data = $this.data()
    name = undefined
    value = undefined
    e = {self: $this}
    $.each(data, (key,val) =>
      key = key.substr(2).toLowerCase()
      if key == "id"
        @elements[val] = e
        if name == undefined
          name = key
      if key == "name"
        name = val
        @e_vals[val] = [] if @e_vals[val] == undefined
        @e_vals[val].push(e)
      else if key.substr(0,2) == "on"
        method = key.substr(2)
        if typeof @[val] == "function"
          $this.bind(method, => @[val]())
      else if key.substr(0,2) == "at"
        attr = key.substr(2)
        e.attr = {} if e.attr == undefined
        e.attr[attr] = val
        @e_attrs[val] = {} if @e_attrs[val] == undefined
        @e_attrs[val][attr] = [] if @e_attrs[val][attr] == undefined
        @e_attrs[val][attr].push(e)
      else
        e[key] = val
        if key == "val"
          value = val
      if name != undefined && value != undefined
        name_arr = name.split(".")
        o = @vals
        i = 0
        while i < name_arr.length - 2
          o = o[name_arr[i]]
          o = {} if o == undefined
          i++
        o[name_arr[i]] = value
  )

  set_elements: ->
    @elements = {}
    self = @
    $("*", @_place).each(
      ->
        self.parse_element($(this))
    )
    @parse_element(@_place)

  get_val: (name) ->
    if name
      @vals[name]
    else
      @vals

  set_val: (name, val, do_not_set) ->
    val = @transform_val(name, val)
    @vals[name] = val
    if !do_not_set
      @iterate_val(name, val || @defaults[name])

  iterate_val: (s, obj) ->
    if typeof obj == "object"
      for key of obj
        @iterate_val s + "." + key, obj[key]
    else
      if @e_vals[s]
        for e in @e_vals[s]
          e.self.html(obj || e.default)
      if @e_attrs[s]
        for attr of @e_attrs[s]
          for e in @e_attrs[s][attr]
            val = @transform_attr(attr, s, obj)
            if attr == "bg"
              e.self.background_image(val || e.default)
            else
              e.self.attr(attr, val || e.default)

  set_vals: (vals, do_not_set) ->
    @reset()
    for key, val of vals
      @set_val(key, val, do_not_set)
    return vals

  transform_val: (name, val) ->
    return val

  transform_attr: (attr, name, val) ->
    return val

  user_is_auth: ->
    return @_app.user_is_auth()

  reset: ->
    @vals = {}

  show: ->
    @_place.show()

  hide: ->
    @_place.hide()

  remove: ->
    @_place.remove()

class FilmThumb extends Item
  constructor: (opts = {}, callback) ->
    @_name = "film-thumb"
    super opts, =>
      ri = @elements["relation.rating"].self
      if !opts.place
        ri.rateit()
      ri
        .rateit "min", 0
        .rateit "max", 10
        .bind("beforerated beforereset", (event) =>
          if !@user_is_auth()
            event.preventDefault()
        )
        .bind "reset rated", (event) => @action_rate(ri.rateit("value"))

  transform_attr: (attr, name, val) ->
    if attr == "href" && name == "id"
      return "/films/" + val
    else
      return val

  transform_val: (name, val) ->
    if name == "releasedate"
      return " (" + val.substr(0, 4) + ")"
    else
      super

  set_vals: (vals, do_not_set) ->
    if vals.locations && vals.locations.length
      @elements["notinstock"].self.hide()
      @elements["instock"].self.show()
      vals.hasFree = false
      vals.price = 0
      for loc in vals.locations
        loc.price = parseFloat(loc.price || 0)
        if loc.price_type == 0
          vals.hasFree = true
        else if loc.price && (vals.price == 0 || loc.price < vals.price)
          vals.price = loc.price
      if vals.hasFree
        @elements["watch_btn"].self.html("Смотреть<br/>Бесплатно").parent().removeClass("button-priced")
        if vals.price
          @elements["watch_price"].self.visible()
        else
          @elements["watch_price"].self.invisible()
      else
        @elements["watch_price"].self.invisible()
        @elements["watch_btn"].self.html('Смотреть<br/><span>от <span class="price">' + loc.price + '</span> р. без рекламы</span>').parent().addClass("button-priced")
    else
      @elements["notinstock"].self.show()
      @elements["instock"].self.hide()
    super

  action_rate: (val) ->
    @_app.film_action @vals.id, "rate", {
      rel: @vals.relation
      value: val
      callback: (new_state) =>
        alert("done")
    }

  toggle_playlist: (status) ->
    @_app.film_action @vals.id, "playlist", {
      rel: @vals.relation
      state: status
      callback: (new_state) =>
        alert("done")
    }

  toggle_notwatch: (status) ->
    @_app.film_action @vals.id, "notwatch", {
      rel: @vals.relation
      state: status
      callback: (new_state) =>
        alert("done")
    }

  toggle_subscribe: (status) ->
    @_app.film_action @vals.id, "subscribe", {
      rel: @vals.relation
      state: status
      callback: (new_state) =>
        alert("done")
    }

  watchfilm: ->
    location.href = "/films/" + @vals.id

class CommentThumb extends Item
  constructor: ->
    @_name = "comment-thumb"
    super

  transform_attr: (attr, name, val) ->
    if attr == "href" && name == "user.id"
      return "/users/" + val
    else
      super

  transform_val: (name, val) ->
    super

  set_vals: (vals, do_not_set) ->
    if vals.created
      if !vals.time_text
        vals.time_text = time_text(new Date(vals.created))
      @elements["time_text"].val = vals.created
    super

class PersonThumb extends Item
  constructor: (opts= {}, callback) ->
    @_name = "person-thumb"
    super

  transform_attr: (attr, name, val) ->
    if attr == "href" && name == "id"
      return "/persons/" + val
    else
      super

class Deck
  constructor: (@_place, opts = {}) ->
    @load_counter = 0
    @page = 0
    @load_func = undefined
    @items = []
    @more = {}

    self = @
    $("." + @element_name, @_place).each(
      ->
        self.add_item_DOM($(this))
    )
    @load_func = opts.load_func if opts.load_func
    if opts.more_place
      @load_more_bind(opts.more_place)

  add_item_DOM: (obj) ->
    @items.push(new @item_class({place: obj, do_not_set: true}))

  add_item: (item) ->
    @items.push(new @item_class({parent: @_place, vals: item}))

  add_items: (items) ->
    for item in items
      @add_item(item)

  get_items: ->
    @items

  load_more_bind: (place) ->
    @more.place = place
    @more.btn = $("button", place)
    @more.btn.click(=> @load_more())

  load_more: (opts) ->
    if @load_func != undefined
      @load_counter++
      @load_func(@, opts)

  load_more_hide: ->
    @more.place.hide() if @more.place

  load_more_show: ->
    @more.place.show() if @more.place

  clear: ->
    @load_counter++
    for item in @items
      item.remove()
    @items = []
    @_place.empty()
    @page = 0

class CommentsDeck extends Deck
  constructor: (place, opts = {}) ->
    @element_name = "comment-thumb"
    @item_class = CommentThumb
    super
    setInterval(
      =>
        @time_update()
      , 5000
    )
    @time_update()

  time_update: ->
    for item in @items
      if item.elements.time_text.val
        item.elements.time_text.self.text(time_text(new Date(item.elements.time_text.val)))

class FilmsDeck extends Deck
  constructor: (place, opts = {}) ->
    @element_name = "film-thumb"
    @item_class = FilmThumb
    super

class PersonsDeck extends Deck
  constructor: (place, opts) ->
    @element_name = "person-thumb"
    @item_class = PersonThumb
    super

class App
  conf = window.mi_conf || {}

  user =
    id: null
    name: ""

  templates = {}
  pages = {}
  active_page = undefined
  query_params = undefined

  constructor: (opts = {}, name) ->
    # App is Singleton
    if window.mi_app
      error "App is already running", "crit"
    window.mi_app = @
    # App we need Rest lib
    if !$.RestClient
      error "No Rest Library found"

    # Extend options with a custom one

    $.extend(conf, opts)

    @rest = new $.RestClient conf.api_url

    @rest.add("user")
    @rest.add("users")
    @rest.users.add("films")
    @rest.users.add("persons")
    @rest.users.add("friendship")
    @rest.users.add("friends")
    @rest.users.add("feed")
    @rest.add("films")
    @rest.films.add("search")
    @rest.films.add("persons")
    @rest.films.add("action", {isSingle: true})
    @rest.films.action.add("rate")
    @rest.films.action.add("subscribe")
    @rest.films.action.add("notwatch")
    @rest.films.action.add("playlist")
    @rest.add("persons")
    @rest.persons.add("filmography", {isSingle: true})
    @rest.persons.add("action", {isSingle: true})
    @rest.persons.action.add("subscribe")

    if name != undefined
      @show_page(name, conf.page_conf)

  film_action: (id, action, opts = {}) ->
    if @user_is_auth()
      rel = opts.rel || {}
      action_str = action
      action_str+= "d" if action == "subscribe"
      new_state = state_toggle(opts.status, rel[action_str])
      if action == "rate"
        if !opts.value
          @rest.films.action.rate.destroy(id)
          .done(
            ->
              rel.rating = false if opts.rel
              opts.callback(false) if opts.callback
          )
        else
          @rest.films.action.rate.update id, {rating: opts.value}
          .done(
            ->
              rel.rating = false if opts.rel
              opts.callback(opts.value) if opts.callback
          )
      else
        if new_state
          doit = "update"
        else
          doit = "destroy"
        @rest.films.action[action][doit](id)
        .done(
          ->
            rel[action_str] = new_state if opts.rel
            opts.callback(new_state) if opts.callback
        )

  person_action: (id, action, opts = {}) ->
    if @user_is_auth()
      rel = opts.rel || {}
      action_str = action
      action_str+= "d" if action == "subscribe"
      new_state = state_toggle(opts.status, rel[action_str])
      if new_state
        doit = "update"
      else
        doit = "destroy"
      @rest.persons.action[action][doit](id)
      .done(
        ->
          rel[action_str] = new_state if opts.rel
          opts.callback(new_state) if opts.callback
      )

  config: (name) ->
    if name == undefined
      return conf
    else
      return conf[name]

  user_is_auth: (ask_sign_in = true) ->
    if !@rest.has_auth()
      if ask_sign_in
        alert("sign in first")
      false
    else
      true

  query_params: (name) ->
    if !query_params
      query_params = $.parseParams()
    if name
      return query_params[name]
    else
      return query_params

  # get template or load it from scratch
  get_tpl: (name, callback) ->
    if templates[name]
      if callback
        callback templates[name]
    else
      ajax_opts =
        url: @config("tpl_url") + name + ".html"
        dataType: "html"
        error: ->
          error "Unable to load template name \"" + name + "\""
          if callback
            callback undefined
        success: (data) =>
          if callback
            callback templates[name] = $(data)
      $.ajax ajax_opts

  # register template with current jQuery object
  register_tpl: (name, jObj) ->
    templates[name] = jObj

  hide_page: (name) ->
    if !_pages[name]
      if active_page == name
        pages[name].hide()
        active_page = undefined
      else
        error "Page " + name + " is not active"
    else
      error "No page " + name + "found"

  show_page: (name, conf) ->
    p = @page(name, conf)
    if p
      active_page = name
      p.show()
    else
      error "No page " + name + "found"

  active_page: ->
    return active_page

  page: (name, conf) ->
    if name == undefined
      name = active_page
    if pages[name]
      return pages[name]
    #try
    page_obj = new (eval("Page_" + name))(conf)
    return pages[name] = page_obj
    #catch
    #  error "Unable to init page " + name, "crit"
    #  return undefined

class Page_Main extends Page
  films_deck = undefined
  self = undefined
  _filter_params = {}
  _filter_counter = 0

  constructor: ->
    # init parent
    self = @
    super
    @_app.get_tpl("film-thumb")
    films_deck = new FilmsDeck($("#films"), {load_func: @load_more_films})
    films_deck.load_more_bind($("#films_more"))
    $(".film-thumb", $("#films_new")).each(
      ->
        new FilmThumb({place: $(this), do_not_set: true})
    )

    @_e.filter =
      parent: $("#frm_filter")
      genre: $("#sel_genre")
      year_old: $("#sel_year_old")
      rating: $("#sel_rating")
      price: $("#sel_price")

    for key, el of @_e.filter
      el.change (=> @filter_changed_event())

    params = @_app.query_params()

    if params
      if params.q
        _filter_params.text = params.q

      for param_name, param_value of params
        for filter_name, filter_obj of @_e.filter
          if filter_name == param_name
            $("option", filter_obj).each(
              ->
                e = $(this)
                e.prop "selected", e.val() == param_value
            )

    @update_filter_params()
    films_deck.load_more()

  filter_changed_event: ->
    @filter_changed()

  filter_changed: (text) ->
    _filter_counter++
    if text != undefined
      _filter_params.text = text
    current_filter_counter = _filter_counter
    setTimeout(
      =>
        if _filter_counter == current_filter_counter
          @update_filter_params()
          opts =
            clear_output: true
            page_loading: false
            params: _filter_params
          @load_more_films(films_deck, opts)
      @_app.config("filter_delay")
    )

  update_filter_params: (update_href = true) ->
    if _filter_params.text
      query_string = "text=" + encodeURI(_filter_params.text)
    else
      query_string=""

    if films_deck.page
      _filter_params.page = films_deck.page
      query_string+= "&" if query_string
      query_string+= "page=" + films_deck.page

    for key, el of @_e.filter
      val = el.val()
      if val && val != "0"
        _filter_params[key] = val
        query_string+= "&" if query_string
        query_string+= key + "=" + val
      else
        _filter_params[key] = null

    query_string = "?" + query_string if query_string
    if update_href
      if history && history.pushState
        history.pushState null, null, query_string

  load_more_films: (deck, opts = {}) ->
    if opts.clear_output
      deck.clear()
    current_counter = deck.load_counter
    deck.load_more_hide()
    opts.params = {} if !opts.params
    self._app.rest.films.read("search", opts.params)
    .done(
      (data) =>
        return if current_counter != deck.load_counter
        if data.items
          deck.add_items(data.items)
        if Math.ceil(data.total_cnt / data.per_page) > data.page
          deck.load_more_show()
          deck.page = data.page
        opts.callback() if opts.callback
    )
    .fail(
      (data) =>
    )

# implementing Login and Register Page class
class Page_Login extends Page

class Page_Registration extends Page
  @constructor: ->
    super
    $("#frm_reg").submit( ->
      return false
    )

class Page_Film extends Page
  film_id = undefined
  films_deck = undefined
  comments_deck = undefined
  actors_deck = undefined
  locations = {}
  params = undefined

  constructor: (@conf) ->
    super
    films_deck = new FilmsDeck($("#films"))
    comments_deck = new CommentsDeck($("#comments"))
    actors_deck = new PersonsDeck($("#actors"), {load_func: => @load_all_actors()})
    actors_deck.load_more_bind($("#actors_more"))

    @_e.rateit = $("#rateit")
    @_e.rateit
    .rateit "min", 0
    .rateit "max", 10
    .bind("beforerated beforereset", (event) =>
      if !@user_is_auth()
        event.preventDefault()
    )
    .bind "reset rated", (event) => @action_rate(@_e.rateit.rateit("value"))

    @_e.notwatch_btn = $("#notwatch_btn")
    @_e.notwatch_btn.bind("click", => @action_notwatch_toggle()) if @_e.notwatch_btn.length
    @_e.playlist_btn = $("#playlist_btn")
    @_e.playlist_btn.bind("click", => @action_playlist_toggle()) if @_e.playlist_btn.length
    @_e.subscribe_btn = $("#subscribe_btn")
    @_e.subscribe_btn.bind("click", => @action_subscribe_toggle()) if @_e.subscribe_btn.length

    self = @
    if @conf.locations && @conf.locations.length
      $(".location-thumb", $("#locations")).each( ->
        $this = $(this)
        id = $this.data("miVal")
        i = 0
        loc = undefined
        while i < self.conf.locations.length && self.conf.locations[i].id != id
          i++
        loc = self.conf.locations[i] if i < self.conf.locations.length
        if loc
          $this.click(-> self.play_location(id))
          $(".type", $this).text(location_type_to_text(loc.type))
          if loc.price_type == 0 || loc.price == 0
            $(".price", $this).text("смотреть бесплатно")
          else
            $(".price", $this).text(loc.price + " р.")
          loc._el = $this
          locations[id] = loc
      )

      @player = new Player($("#player"))
      @player.clear()

      loc_id = @_app.query_params("loc")
      if !loc_id
        for key,item of locations
          if item.price_type == 0
            loc_id = key
      @play_location(loc_id) if loc_id

  play_location: (id) ->
    @player.load(locations[id]) if locations[id]

  load_all_actors: () ->
    actors_deck.load_more_hide();
    @_app.rest.films.persons.read(@conf.id, {type: "a", top: actors_deck.get_items().length})
    .done(
      (data)=>
        if data && data.length
          actors_deck.add_items(data)
    )

  action_rate: (val) ->
    @_app.film_action @conf.id, "rate", {
      rel: @conf.relation
      value: val
      callback: (new_value) =>
        alert("done")
    }

  action_notwatch_toggle: (status) ->
    @_app.film_action(@conf.id, "notwatch", {
      state: status
      rel: @conf.relation
      callback: =>

    })

  action_subscribe_toggle: (status) ->
    @_app.film_action(@conf.id, "subscribe", {
      state: status
      rel: @conf.relation
      callback: =>
    })

  action_playlist_toggle: (status) ->
    @_app.film_action(@conf.id, "playlist", {
      state: status
      rel: @conf.relation
      callback: =>
    })

class Page_Person extends Page
  films_deck = undefined
  constructor: (@conf) ->
    super
    films_deck = new FilmsDeck($("#films"), {load_func: (deck) =>@load_more_films(deck) })
    films_deck.load_more_bind($("#films_more"))
    @_e.subscribe_btn = $("#subscribe_btn").click(=> @action_subscribe())

  action_subscribe: (status) ->
    @_app.person_action(@conf.id, "subscribe", {
      rel: @conf.relation
      status: status
      callback: =>
        alert("done")
    })

  load_more_films: (deck) ->
    current_counter = deck.load_counter
    deck.load_more_hide()
    @_app.rest.persons.filmography.read(@conf.id, {})
    .done(
      (data) =>
        return if current_counter != deck.load_counter
        if data.items
          deck.add_items(data.items)
        if Math.ceil(data.total_cnt / data.per_page) > data.page
          deck.load_more_show()
          deck.page = data.page
    )
    .fail(
      (data) =>
    )

class Page_Playlist extends Page
  film = undefined
  comments_deck = undefined
  actors_deck = undefined
  locations = {}

  constructor: (@conf) ->
    super
    comments_deck = new CommentsDeck($("#comments"))
    actors_deck = new PersonsDeck($("#actors"), {load_func: => @load_all_actors()})
    actors_deck.load_more_bind($("#actors_more"))

    @_e.rateit = $("#rateit")
    @_e.rateit
    .rateit "min", 0
    .rateit "max", 10
    .bind("beforerated beforereset", (event) =>
      if !@user_is_auth()
        event.preventDefault()
    )
    .bind "reset rated", (event) => @action_rate(@_e.rateit.rateit("value"))

    @_e.notwatch_btn = $("#notwatch_btn")
    @_e.notwatch_btn.bind("click", => @action_notwatch_toggle()) if @_e.notwatch_btn.length
    @_e.playlist_btn = $("#playlist_btn")
    @_e.playlist_btn.bind("click", => @action_playlist_toggle()) if @_e.playlist_btn.length
    @_e.subscribe_btn = $("#subscribe_btn")
    @_e.subscribe_btn.bind("click", => @action_subscribe_toggle()) if @_e.subscribe_btn.length

    self = @
    film = @conf.film
    if film.locations && film.locations.length
      $(".location-thumb", $("#locations")).each( ->
        $this = $(this)
        id = $this.data("miVal")
        i = 0
        loc = undefined
        while i < film.locations.length && film.locations[i].id != id
          i++
        loc = film.locations[i] if i < film.locations.length
        if loc
          $this.click(-> self.play_location(id))
          $(".type", $this).text(location_type_to_text(loc.type))
          if loc.price_type == 0 || loc.price == 0
            $(".price", $this).text("смотреть бесплатно")
          else
            $(".price", $this).text(loc.price + " р.")
          loc._el = $this
          locations[id] = loc
      )

      @player = new Player($("#player"))
      @player.clear()

      loc_id = @_app.query_params("loc")
      if !loc_id
        for key,item of locations
          if item.price_type == 0
            loc_id = key
      @play_location(loc_id) if loc_id

  play_location: (id) ->
    @player.load(locations[id]) if locations[id]

  load_all_actors: () ->
    actors_deck.load_more_hide();
    @_app.rest.films.persons.read(film.id, {type: "a", top: actors_deck.get_items().length})
    .done(
      (data)=>
        if data && data.length
          actors_deck.add_items(data)
    )

  action_rate: (val) ->
    @_app.film_action film.id, "rate", {
      rel: @conf.relation
      value: val
      callback: (new_value) =>
        alert("done")
    }

  action_notwatch_toggle: (status) ->
    @_app.film_action(film.id, "notwatch", {
      state: status
      rel: @conf.relation
      callback: =>

    })

  action_subscribe_toggle: (status) ->
    @_app.film_action(film.id, "subscribe", {
      state: status
      rel: @conf.relation
      callback: =>
    })

  action_playlist_toggle: (status) ->
    @_app.film_action(film.id, "playlist", {
      state: status
      rel: @conf.relation
      callback: =>
    })

window.InitApp =  (opts = {}, page_name) ->
  new App(opts, page_name)
  delete window.InitApp