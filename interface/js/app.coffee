'use strict'

window.App = undefined

conf =
  no_poster_url: "img/noposter.jpg"
  filter_delay: 1000
  api_url: 'api/'
  tpl_prefix: 'jade/_part_'

error = (txt, type = "norm") ->
  if type == "crit"
    throw new Error "CRITICAL ERROR: " + txt
  else
    console.log "ERROR: " + txt

check_app_is_init = (c) ->
  if !window.App
    error "App is not init", "crit"
  else
    c._app = window.App

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

# basic class
class Item
  constructor: (opts = {}, callback = undefined) ->
    check_app_is_init(@)
    if (!@_name)
      error "It's wrong to use parent class", "crit"
    if opts.place == undefined
      @_place = $('<span class="preload_' + @_name + '"></span>')
      if opts.parent
        @_place.appendTo(opts.parent)
      @_app.get_tpl(
        @_name
        (tpl_obj) =>
          if tpl_obj
            old_place = @_place
            @_place = tpl_obj.clone()
            @set_vals opts.vals if opts.vals
            @_place.insertAfter(old_place)
            old_place.remove()
            callback @ if callback
          else
            error 'Unable to load template for object "' + @_name + '"'
      )
    else
      @_place = opts.place
      @set_vals opts.vals if opts.vals
      callback @ if callback

  place: ->
    @_place

  vals: (name) ->
    if name
      @_vals[name]
    else
      @_vals

  set_vals: (vals) ->
    $.extend @reset(), vals
    if vals._do_not_set == undefined
      for k,v of vals
        $("." + @_name + "-" + k, @_place).html(v)

  user_is_auth: ->
    # check user is auth
    true

  reset: ->
    @_vals = {}

  show: ->
    @_place.show()

  hide: ->
    @_place.hide()

  remove: ->
    @_place.remove()

# a Film class
class Film extends Item
  constructor: (opts = {}, callback) ->
    @_name = "afilm"
    opts.vals = {} if opts.vals == undefined
    if opts && opts.place
      opts.vals._do_not_set = true
      opts.vals.id = opts.place.attr("id").substr(4)
      opts.vals.poster = $(".afilm-poster", opts.place).attr("src")
      opts.vals.name = $(".afilm-name", opts.place).text()
      opts.vals.year = $(".afilm-year", opts.place).text()
      opts.vals.watchtext = $(".afilm-watchtext", opts.place).text()
      opts.vals.rating = $(".afilm-rating", opts.place).text()
      opts.vals.relation =
        rating: $(".rateit", opts.place).rateit("value")

    opts.vals.rating = opts.vals.ratings.cons if opts.vals.ratings && opts.vals.ratings.cons
    opts.vals.year = opts.vals.release_date.substr(0, 4) if opts.vals.release_date
    if opts.vals.locations
      loc_free = false
      loc_min_price = null
      for loc in opts.vals.locations
        if loc.price_type == "f"
          loc_free = true
        else
          if loc.price && (loc_min_price == null || loc_min_price > loc.price)
            loc_min_price = loc.price
      opts.vals.watchtext = ""
      if loc_free
        opts.vals.watchtext = "бесплатно"
        opts.vals.watchtext+= "<span> или</span><br/>" if loc_min_price
      if loc_min_price
        opts.vals.watchtext+= "от " + loc_min_price + "р. без рекламы"
    else
      delete opts.vals.watchtext
    super opts, =>
      if !opts.place
        $(".rateit", @_place).rateit()
      ri = $(".rateit", @_place)
      ri
        .rateit "min", 0
        .rateit "max", 10
        .bind("beforerated beforereset", (event) =>
          if !@user_is_auth()
            alert "You have to be signed"
            event.preventDefault()
        )
        .bind "reset rated", (event) => @action_rate(ri.rateit("value"))
      rel = @vals("relation")
      if rel
        if rel.rating != undefined
          rInt = Math.floor(rel.rating)
          rFloor = 0
          rFloor = 0.5 if rel.rating - rInt > 0.5
          ri.rateit "value", rInt + rFloor
      $(".afilm-tolist", @_place).click => @action_toggle_subscribe()

      callback @ if callback

  action_toggle_subscribe: (status) ->
    if @user_is_auth()
      rel = @vals("relation")
      if status != undefined
        new_subscribed = status
      else
        new_subscribed = true
        if rel && rel.subscribed
            new_subscribed = false

      if new_subscribed
        action = "update"
      else
        action = "destroy"
      @_app.rest.films.action.subscribe[action](@vals("id"))
        .done(
          ->
            rel.subscribed = new_subscribed
        )

  action_rate: (val) ->
    if @user_is_auth()
      @_app.rest.films.action.rate.update @vals("id"), {rating: val}

  reset: ->
    @_vals =
      id: null
      name: null
      poster: null
      year: null
      rating: null
      user: null
      watchtext: null

  set_vals: ->
    super
    @_place.attr("id", "film" + @_vals.id)
    $(".afilm-name", @_place).attr("href", "/films/" + @_vals.id)
    $(".afilm-poster", @_place).attr("src", @_vals.poster || conf.no_poster_url)
    if @_vals.rating
      $(".afilm-rating", @_place).visible()
    else
      $(".afilm-rating", @_place).invisible()
    if @_vals.watchtext
      $(".afilm-watchtext-place", @_place).visible()
    else
      $(".afilm-watchtext-place", @_place).invisible()

# a Person class
class Person
  constructor: (@parent) ->
    checkAppIsInit(@)

# a User class
class User
  constructor: (@parent) ->
    checkAppIsInit(@)

class App
  _options =
    api_url: 'api/'
    tpl_prefix: 'jade/_part_'

  _user =
    id: null
    name: ""

  _templates = {}
  _pages = {}
  _active_page = undefined
  _query_params = undefined

  opts: (name) ->
    if name
      @_options[name]
    else
      @_options

  constructor: (opts = {}, name) ->
    # App is Singleton
    if window.App
      error "App is already running", "crit"
    window.App = @
    # App we need Rest lib
    if !$.RestClient
      error "No Rest Library found"

    # Extend options with a custom one
    $.extend(_options, opts)

    @rest = new $.RestClient conf.api_url

    @rest.add("user")
    @rest.add("users")
    @rest.add("films")
#    @rest.films.add("search")
    @rest.films.add("action", {isSingle: true})
    @rest.films.action.add("rate")
    @rest.films.action.add("subscribe")
    @rest.films.action.add("notwatch")
    @rest.add("persons")
    @rest.persons.add("filmography", {isSingle: true})

    # TODO autoauth user

    @_e = {}
    # TODO init search place
    @_e.search =
      form: $("#frm_search").submit(-> return false)
      input: $("#inp_search").keydown(=> @search_keydown)
      button: $("#inp_button").click(=> @search_submit(); return false)

    # TODO init user place
    @_e.user_reg =
      place: $("#usr_reg_place")

    @_e.user_guest =
      place: $("#usr_guest_place")

    # init elements
    @_e.search.input.val(@query_params("text") || "")

    if name != undefined
      @show_page(name, opts.page_conf)

  search_keydown: (event) ->
    if event.which == 13 # enter pressed
      @_e.search.button.click()
      return
    if event.which == 27 # esc pressed
      @_e.input.val("").focus()

  search_submit: ->
    text = @_e.search.input.val() || ""
    if _active_page == "Mai1n" # current page is main
      @page().filter_changed text
    else
      text = "?text=" + text if text
      window.location.href = "/" + text

  query_params: (name) ->
    if !_query_params
      _query_params = $.parseParams()
    if name
      return _query_params[name]
    else
      return _query_params

  # get template or load it from scratch
  get_tpl: (name, callback) ->
    if _templates[name]
      if callback
        callback _templates[name]
    else
      ajax_opts =
        url: conf.tpl_prefix + name + ".html"
        dataType: "html"
        error: ->
          error "Unable to load template name \"" + name + "\""
          if callback
            callback undefined
        success: (data) =>
          if callback
            callback _templates[name] = $(data)
      $.ajax ajax_opts

  # register template with current jQuery object
  register_tpl: (name, jObj) ->
    _templates[name] = jObj

  hide_page: (name) ->
    if !_pages[name]
      if _active_page == name
        _pages[name].hide()
        _active_page = undefined
      else
        error "Page " + name + " is not active"
    else
      error "No page " + name + "found"

  show_page: (name, conf) ->
    p = @page(name, conf)
    if p
      _active_page = name
      p.show()
    else
      error "No page " + name + "found"

  active_page: ->
    return _active_page

  page: (name, conf) ->
    if name == undefined
      name = _active_page
    if _pages[name]
      return _pages[name]
    #try
    page_obj = new (eval("Page_" + name))(conf)
    return _pages[name] = page_obj
    #catch
    #  error "Unable to init page " + name, "crit"
    #  return undefined


# implementing Main Page class
class Page_Main extends Page
  _films = []
  _current_page = 0
  _load_counter = 0
  _filter_counter = 0

  _filter_params = {}

  constructor: ->
    # init parent
    super
    # save places
    @_e.output_place = $("#output_place")
    @_e.filter =
      genre: $("#fil_genre")
      year_old: $("#fil_year_old")
      rating: $("#fil_rating")
      price: $("#fil_price")

    for key, el of @_e.filter
      el.change (=> @filter_changed_event())

    @_e.loadmore =
      place: $("#load-more-place")
      btn: $("#btn_loadmore").click(=> @load_more())

    @_app.get_tpl("afilm")
# set filter params
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

# parse already exists films
    $(".afilm-place", @_e.output_place).each(
      ->
        _films.push new Film({place: $(this)})
    )

    @load_more() if _films.length < 12

  filter_changed_event: ->
    @filter_changed()

  filter_changed: (text) ->
    _filter_counter++
    if text
      _filter_params.text = text || ""
    current_filter_counter = _filter_counter
    setTimeout(
      =>
        if _filter_counter == current_filter_counter
          @update_filter_params()
          opts =
            clear_output: true
            page_loading: false
            params: _filter_params
          @load_films(opts)
      conf.filter_delay
    )

  load_more: (page_cnt = 1) ->
    @_e.loadmore.btn.prop('disabled', true);
    opts =
      clear_output: false
      page_loading: true
      params: _filter_params

    @load_films opts

  update_filter_params: (update_href = true) ->
    if _filter_params.text
      query_string = "text=" + encodeURI(_filter_params.text)
    else
      query_string=""

    if _current_page
      _filter_params.page = _current_page
      query_string+= "&" if query_string
      query_string+= "page=" + _current_page

    for key, el of @_e.filter
      val = el.val()
      if val && val != "0"
        _filter_params[key] = val
        query_string+= "&" if query_string
        query_string+= key + "=" + val

    query_string = "?" + query_string if query_string
    if update_href
      if history && history.pushState
        history.pushState null, null, query_string

  load_films: (opts = {}) ->
    _load_counter++;
    current_counter = _load_counter

    if opts.clear_output
      i = 0
      while i < _films.length
        delete _films[i]
        i++

      _films = []
      @_e.output_place.empty()

    if !opts.page_loading
      @_e.loadmore.place.hide()

    opts.params = {} if !opts.params
    @_app.rest.films.read("search", opts.params)
      .done(
        (data) =>
          return if current_counter != _load_counter
          if data.items
            for item in data.items
              _films.push new Film({parent: @_e.output_place, vals: item})
          if Math.ceil(data.total_cnt / data.per_page) > data.page
            @_e.loadmore.place.show()
            @_e.loadmore.btn.prop('disabled', false);
          _current_page = data.page
          opts.callback() if opts.callback
      )
      .fail(
        (data) =>
      )

# implementing Login and Register Page class
class Page_Login extends Page

class Page_Register extends Page

class Page_Person extends Page
  _films = []
  _current_page = 0
  _load_counter = 0

  constructor: (opts = {}) ->
    @person_id = opts.person_id
    super
    @_e.films_place = $("#films")

    @_e.loadmore =
      place: $("#load-more-place")
      btn: $("#btn_loadmore").click(=> @load_more())

    @_app.get_tpl("afilm")

    $(".afilm-place", @_e.films_place).each(
      ->
        _films.push new Film({place: $(this)})
    )

    @load_more() if _films.length < 12

  load_more: (page_cnt = 1) ->
    @_e.loadmore.btn.prop('disabled', true);
    _load_counter++
    current_counter = _load_counter


    @_e.loadmore.place.hide()
    @_app.rest.persons.filmography.read(@person_id, {})
    .done(
      (data) =>
        return if current_counter != _load_counter
        if data.items
          for item in data.items
            _films.push new Film({parent: @_e.films_place, vals: item})
        if Math.ceil(data.total_cnt / data.per_page) > data.page
          @_e.loadmore.place.show()
          @_e.loadmore.btn.prop('disabled', false);
        _current_page = data.page
    )
    .fail(
      (data) =>
    )

window.InitApp =  (opts = {}, page_name) ->
  new App(opts, page_name)
  delete window.InitApp