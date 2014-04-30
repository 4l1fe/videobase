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


class Location
  obj = undefined

  constructor: (@parent, @vals) ->

  show: ->
    if obj == undefined
      html = undefined
      if @vals.type == "ivi"
        html = '<iframe src="http://www.ivi.ru/external/stub?videoId=' + @vals.value + '&subsiteId=138" width="860" height="480" frameborder="0"></iframe><div style="top:-200px; z-index:-1; position: relative;">'
      else if @vals.type == "now"
        html = '<iframe name="now1028482" src="http://www.now.ru/embed/frame/' + @vals.value + '" scrolling="no" frameborder="no" height="480" width="860"></iframe>'
      else if @vals.type == "megogo"
        html = '<iframe width="850" height="480" src="http://megogo.net/e/' + @vals.value + '" frameborder="0" allowfullscreen></iframe>'
      else if @vals.type == "tvigle"
        html = '<object type="application/x-shockwave-flash" data="http://www.tvigle.ru//swf/tvigle_v12.swf?ver=3.5919999999999757" width="860" height="480" id="plr" style="visibility: visible;"><param name="allowScriptAccess" value="always"><param name="bgcolor" value="#000000"><param name="quality" value="high"><param name="scale" value="noscale"><param name="allowFullScreen" value="true"><param name="wmode" value="transparent"><param name="flashvars" value="ref=1&amp;obj=' + @vals.value + '&amp;cnl=1882&amp;sid_name=&amp;user_sid=&amp;own=0&amp;w=860&amp;h=480&amp;ap=1&amp;afbr=1&amp;region=RU&amp;skin=&amp;d=tvigle.ru"></object>'
      if html == undefined
        console.log("Error: unknown location type")
        html = '<img src=@_app.config("noposter_url") />'
      obj = $(html).appendTo(@parent).show()

  hide: ->
    if obj != undefined
      obj.hide()

  reset: ->
    if obj == undefined
      return
    obj.remove()
    obj = undefined

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

# basic class
class Item
  constructor: (opts = {}, callback = undefined) ->
    check_app_is_init(@)
    if (!@_name)
      error "It's wrong to use parent class", "crit"
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
        $("." + k, @_place).html(v)

  user_is_auth: ->
    alert "Sign in first"
    return @_app.user_is_auth()

  reset: ->
    @_vals = {}

  show: ->
    @_place.show()

  hide: ->
    @_place.hide()

  remove: ->
    @_place.remove()

# a Film class
class FilmThumb extends Item
  constructor: (opts = {}, callback) ->
    @_name = "film-thumb"
    opts.vals = {} if opts.vals == undefined
    if opts && opts.place
      opts.vals._do_not_set = true
      opts.vals.id = opts.vals.id || opts.place.attr("id").substr(11)
      opts.vals.poster = $(".poster-place", opts.place).background_image()
      opts.vals.name = $(".name", opts.place).text()
      opts.vals.year = $(".year", opts.place).text().substr(1,4)
      opts.vals.rating = $(".rating", opts.place).text()
      opts.vals.relation =
        rating: $(".rateit", opts.place).rateit("value")
    opts.vals.rating = opts.vals.ratings.cons[0] if (opts.vals.ratings && opts.vals.ratings.cons)
    opts.vals.year = " (" + opts.vals.releasedate.substr(0, 4) + ")" if opts.vals.releasedate
    if $(".notinstock", opts.place).hasClass("display-none")
      if !$(".watchprice", opts.place).hasClass("invisible")
        opts.vals.price = $(".watchprice .price", opts.place).text()
      if $(".watchbtn .price", opts.place).length
        opts.vals.price = $(".watchbtn .price", opts.place).text()
      else
        opts.vals.hasFree = true
    if opts.vals.locations
      opts.vals.hasFree = false;
      opts.vals.price = 0;
      for loc in opts.vals.locations
        if loc.price_type == "f"
          opts.vals.hasFree = true
        else
          if loc.price && (opts.vals.price == 0 || opts.vals.price > loc.price)
            opts.vals.price = loc.price
    super opts, =>
      if !opts.place
        $(".rateit", @_place).rateit()
      ri = $(".rateit", @_place)
      ri
        .rateit "min", 0
        .rateit "max", 10
        .bind("beforerated beforereset", (event) =>
          if !@user_is_auth()
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
      $(".notwatch-btn", @_place).click => @action_toggle_notwatch()
      $(".notinstock button.subscribe-btn", @_place).click => @action_toggle_subscribe()
      $(".playlist-btn", @_place).click => @action_toggle_playlist()
      callback @ if callback

  action_toggle_playlist: (status) ->
    if @user_is_auth()
      rel = @vals("relation")
      if status != undefined
        new_playlist = status
      else
        new_playlist = true
        if rel && rel.playlist
          new_playlist = false

      if new_playlist
        action = "update"
      else
        action = "destroy"
      @_app.rest.films.action.playlist[action](@vals("id"))
      .done(
        ->
          rel.playlist = new_playlist
      )

  action_toggle_notwatch: (status) ->
    if @user_is_auth()
      rel = @vals("relation")
      if status != undefined
        new_notwatch = status
      else
        new_notwatch = true
        if rel && rel.notwatch
          new_notwatch = false

      if new_notwatch
        action = "update"
      else
        action = "destroy"
      @_app.rest.films.action.notwatch[action](@vals("id"))
      .done(
        ->
          rel.notwatch = new_notwatch
      )

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
      hasFree: null
      price: null

  set_vals: ->
    super
    @_place.attr("id", @name + "-" + @_vals.id)
    $(".name", @_place).attr("href", "/films/" + @_vals.id)
    $(".poster-place", @_place).background_image(@_vals.poster || @_app.config("noposter_url"))

    if @_vals.rating
      $(".rating-place", @_place).visible()
    else
      $(".rating-place", @_place).invisible()
    if @_vals.hasFree || @_vals.price
      instock = $(".instock", @_place)
      instock.removeClass("display-none")
      $(".notinstock", @_place).addClass("display-none")
      if @_vals.hasFree
        $("button.watch-btn", instock).html("смотреть<br/>бесплатно")
        if @_vals.price
          $(".watchprice", instock).visible();
          $("button", instock).addClass("action-priced")
      else
        $("button.watchbtn", instock).html("СМОТРЕТЬ <br/><span>от <span class=\"price\">" + @_vals.price + "</span> р. без рекламы</span>")
    else
      $(".instock", @_place).addClass("display-none")
      $(".notinstock", @_place).removeClass("display-none")

# a Person class
class PersonThumb extends Item
  constructor: (opts = {}, callback) ->
    @_name = "person-thumb"
    opts.vals = {} if opts.vals == undefined
    if opts && opts.place
      opts.vals._do_not_set = true
      opts.vals.id = opts.vals.id || opts.place.attr("id").substr(13)
      opts.vals.photo = $(opts.place).background_image()
      opts.vals.name = $(".name", opts.place).text()
    super opts, =>
      callback @ if callback

  reset: ->
    @_vals =
      id: null
      name: null
      photo: null

  set_vals: ->
    super
    @_place.attr("id", @_name + "-" + @_vals.id)
    $(".name", @_place).attr("href", "/person/" + @_vals.id)
    $(@_place).background_image(@_vals.photo || @_app.config("noperson_url"))

# a Comment class
class CommentThumb extends Item
  constructor: (opts = {}, callback) ->
    @_name = "comment-thumb"
    opts.vals = {} if opts.vals == undefined
    if opts && opts.place
      opts.vals._do_not_set = true
      opts.vals.id = opts.vals.id || opts.place.attr("id").substr(13)
      opts.vals.photo = $(opts.place).background_image()
      opts.vals.name = $(".name", opts.place).text()
    super opts, =>
      callback @ if callback

  reset: ->
    @_vals =
      id: null
      name: null
      photo: null

  set_vals: ->
    super
    @_place.attr("id", @_name + "-" +  @_vals.id)
    $(".name", @_place).attr("href", "/person/" + @_vals.id)
    $(@_place).css("background-image", 'url("' + (@_vals.photo || conf.no_person_url) + '")')

# a Feed class
class FeedThumb extends Item
  constructor: (opts = {}, callback) ->
    @_name = "feed-thumb"
    opts.vals = {} if opts.vals == undefined
    if opts && opts.place
      opts.vals._do_not_set = true
      opts.vals.id = opts.vals.id || opts.place.attr("id").substr(10)
      cls = $(".record", opts.place).attr("class").split(" ")
      for key of cls
        if cls[key] != "feed-thumb"
          opts.vals.type = cls[key].substr(5)
    super opts, =>
      need_class = "feed-" + opts.vals.type
      $(".record", @_place).each(
        ->
          el = $(this)
          if !el.hasClass(need_class)
            el.parent().remove()
      )

  reset: ->
    @_vals =
      id: null
      user: null
      object: null

  set_vals: ->
    super
    if @_vals._do_not_set
      return
    @_place.attr("id", @_name + "-" + @_vals.id)
    $(".time", @_place).text(time_text(new Date(@_vals.created)))
    if @_vals.type == "film-o"
      $(".image", @_place).background_image(@_vals.object.poster || @_app.config("noposter_url"))
      $(".cont-place a", @_place).attr("href", "/films/" + @_vals.object.id)
    else if @_vals.type == "pers-o"
      $(".image", @_place).background_image(@_vals.object.photo || @_app.config("noperson_url"))
      $(".film-info a", @_place).attr("href", "/films/" + @_vals.object.film.id).text(@_vals.object.film.name)
      $(".type-" + @_vals.type, @_place).removeClass("display-none")
    else if @_vals.type == "sys-a"
      # something here
    else
      console.log @_vals.user.name
      $(".image", @_place).background_image(@_vals.user.avatar || @_app.config("noavatar_url"))
      $(".info-place .name a", @_place).attr("href", "/users/" + @_vals.user.id).text(@_vals.user.name)
      if @_vals.type.substr(0,4) == "film"
        console.log @_vals.object
        $(".film-info a", @_place).attr("href", "/films/" + @_vals.object.id).text(@_vals.object.name)
        if @_vals.type == "film-c"
          $(".text", @_place).text(@_vals.object.text)
        else if @_vals.type == "film-r"
          console.log (1)
            # do something with rating
      else if @_vals.type == "pers-s"
        $(".photo", @_place).background_image(@_vals.object.photo || @_app.config("noperson_url"))
        $(".person-info a", @_place).attr("href", "/persons/" + @_vals.object.id).text(@_vals.object.name)
      else if @_vals.type.substr(0,4) == "user"
        $(".avatar", @_place).background_image(@_vals.object.avatar || @_app.config("noavatar_url"))
        $(".cont-place .name a", @_place).attr("href", "/users/" + @_vals.object.id).text(@_vals.object.name)

# a User class
class User
  constructor: (@parent) ->
    checkAppIsInit(@)

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
    if window.me_app
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
#    @rest.films.add("search")
    @rest.films.add("persons")
    @rest.films.add("action", {isSingle: true})
    @rest.films.action.add("rate")
    @rest.films.action.add("subscribe")
    @rest.films.action.add("notwatch")
    @rest.films.action.add("playlist")
    @rest.add("persons")
    @rest.persons.add("filmography", {isSingle: true})

    # TODO autoauth user

    @_e = {}
    # TODO init search place
    @_e.search =
      form: $("#frm_search").submit(=> @search_submit(); return false)
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
      @show_page(name, conf.page_conf)

  config: (name) ->
    if name == undefined
      return conf
    else
      return conf[name]

  user_is_auth: ->
    return false

  search_keydown: (event) ->
    if event.which == 13 # enter pressed
      @_e.search.button.click()
      return
    if event.which == 27 # esc pressed
      @_e.input.val("").focus()

  search_submit: ->
    text = @_e.search.input.val() || ""
    if active_page == "Main" # current page is main
      @page().filter_changed text
      $(window).scrollTop(@page()._e.filter.parent.offset().top)
    else
      if text
        window.location.href = "/?text=" + text + "#filter"

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


# implementing Main Page class
class Page_Main extends Page
  _films = []
  _films_new = []
  _current_page = 0
  _load_counter = 0
  _filter_counter = 0

  _filter_params = {}

  constructor: ->
    # init parent
    super
    # save places
    @_e.films = $("#films")
    @_e.filter =
      parent: $("#frm_filter")
      genre: $("#sel_genre")
      year_old: $("#sel_year_old")
      rating: $("#sel_rating")
      price: $("#sel_price")

    for key, el of @_e.filter
      el.change (=> @filter_changed_event())

    @_e.loadmore =
      place: $("#films_more_place")
      btn: $("#films_more_btn").click(=> @load_more())

    @_app.get_tpl("film-thumb")
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
    $(".film-thumb", @_e.films).each(
      ->
        _films.push new FilmThumb({place: $(this)})
    )

    $(".film-thumb", $("#films_new")).each(
      ->
        _films_new.push new FilmThumb({place: $(this)})
    )

    @load_more() if _films.length < 12

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
          @load_films(opts)
      @_app.config("filter_delay")
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
      else
        _filter_params[key] = null

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
      @_e.films.empty()

    if !opts.page_loading
      @_e.loadmore.place.hide()

    opts.params = {} if !opts.params
    @_app.rest.films.read("search", opts.params)
      .done(
        (data) =>
          return if current_counter != _load_counter
          if data.items
            for item in data.items
              _films.push new FilmThumb({parent: @_e.films, vals: item})
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

class Page_Registration extends Page
  @constructor: ->
    super
    $("#frm_reg").submit( ->
      return false
    )

class Page_Person extends Page
  _films = []
  _current_page = 0
  _load_counter = 0
  _opts = {}

  constructor: (opts = {}) ->
    _opts = opts
    @person_id = opts.id
    super
    @_e.films_place = $("#films")

    @_e.loadmore =
      place: $("#load-more-place")
      btn: $("#btn_loadmore").click(=> @load_more())

    @_app.get_tpl("film-thumb")

    $(".film-thumb", @_e.films_place).each(
      ->
        _films.push new FilmThumb({place: $(this)})
    )

    @load_more() if _films.length < 12

    @_e.subscribe = $("#subscribe_btn").click => @action_subscribe_toggle()

  action_subscribe_toggle: (status) =>
    if @user_is_auth()
      rel = _opts.relation || {}
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
      @_app.rest.films.action.subscribe[action](_opts.id)
      .done(
        ->
          rel.subscribed = new_subscribed
      )

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
            _films.push new FilmThumb({parent: @_e.films_place, vals: item})
        if Math.ceil(data.total_cnt / data.per_page) > data.page
          @_e.loadmore.place.show()
          @_e.loadmore.btn.prop('disabled', false);
        _current_page = data.page
    )
    .fail(
      (data) =>
    )

class Page_Film extends Page
  locations = []
  current_location = null
  films = []
  actors = []
  opts = {}

  constructor: (new_opts = {}) ->
    super
    opts = new_opts
    @_app.get_tpl("film-thumb")
    @_app.get_tpl("person-thumb")
    @_e =
      player: $("#player")
    #if opts.locations
      #$(opts.locations).each(
      #  (key, item) =>
      #    el = $("#loc_thumb_" + item.id)
      #    if el.length
      #      locations[item.id] = new Location @_e.pleer_place, item
      #      $("button", el).click(=>
      #        @set_location item.id
      #      )
      #)


    @_e.films = $("#films")
    $(".film-thumb", @_e.films).each(->
       films.push new FilmThumb({place: $(this)})
    )

    @_e.actors = $("#actors")
    $(".person-thumb", @_e.actors).each(->
      actors.push new PersonThumb({place: $(this)})
    )

    @_e.btn_moreactors = $("#btn_moreactors");
    @_e.btn_moreactors.click(
      =>
        @load_actors()
    )

    loc = @_app.query_params("loc")
    if loc && locations[loc]
      @set_location(loc)

  set_location: (id) ->
    if current_location == id
      return
    if current_location != null
      locations[current_location].reset()
    locations[current_location = id].show()

  load_actors: ->
    @_e.btn_moreactors.parent().hide()
    @_app.rest.films.persons.read(opts.id, {type: "a"})
      .done(
        (data)=>
          if data && data.length
            for item in data
              i = 0
              while i < actors.length && actors[i].id != item.id
                i++
              if i >= actors.length
                actors.push(new PersonThumb({parent: @_e.actors, vals: item}))
      )


  load_more_comments: ->
    #pass


class Page_User extends Page
  _friends = []
  _films_subscribed = []
  _films_subscribed_page = 1
  _feed = []
  _feed_page = 0
  _actors = []
  _directors = []
  _opts = {}

  constructor: (opts = {}) ->
    _opts = opts
    @user_id = opts.id
    super

    @_e.films_subscribed = $("#films_subscribed")
    @_e.more_films_subscribed =
      place: $("#more_films_subscribed_place")
      btn: $("#more_films_subscribed").click(=> @load_more_films_subscribed())

    @_e.actors_fav = $("#actors_fav")
    @_e.more_actors_fav =
      place: $("#more_actors_fav_place")
      btn: $("#more_actors_fav").click(=> @load_more_actors_fav())

    @_e.directors_fav = $("#directors_fav")
    @_e.more_directors_fav =
      place: $("#more_directors_fav_place")
      btn: $("#more_directors_fav").click(=> @load_more_directors_fav())

    @_e.feed = $("#feed_place")
    @_e.more_feed =
      place: $("#more_feed_place")
      btn: $("#more_feed_btn").click(=> @load_more_feed())
    @_app.get_tpl("film-thumb")
    @_app.get_tpl("person-thumb")
    @_app.get_tpl("feed-thumb")

    $(".film-thumb", @_e.films_subscribed).each(
      ->
        _films_subscribed.push new FilmThumb({place: $(this)})
    )
    @load_more_films_subscribed() if _films_subscribed.length < 12

    $(".person-thumb", @_e.actors_fav).each(->
      _actors.push new PersonThumb({place: $(this)})
    )

    $(".person-thumb", @_e.directors_fav).each(->
      _directors.push new PersonThumb({place: $(this)})
    )

    $(".feed-thumb", @_e.feed).each(->
      _feed.push new FeedThumb({place: $(this), vals: {_do_not_set: true}})
    )


  load_more_films_subscribed: (page_cnt = 1) ->
    @_e.more_films_subscribed.btn.prop('disabled', true);
    @_e.more_films_subscribed.place.hide()
    _films_subscribed_page++;
    @_app.rest.users.films.read(@user_id, {page: _films_subscribed_page})
    .done(
      (data) =>
        if data.items
          for item in data.items
            _films_subscribed.push new FilmThumb({parent: @_e.films_subscribed, vals: item})
        if Math.ceil(data.total_cnt / data.per_page) > data.page
          @_e.more_films_subscribed.place.show()
          @_e.more_films_subscribed.btn.prop('disabled', false);
        _films_subscribed_page = data.page
    )
    .fail(
      (data) =>
    )

  load_more_actors_fav:->
    @_e.more_actors_fav.place.hide()
    @_app.rest.users.persons.read(_opts.id, {type: "a"})
      .done(
        (data)=>
          if data && data.length
            for item in data
              i = 0
              while i < _actors.length && _actors[i].id != item.id
                i++
              if i >= _actors.length
                _actors.push(new PersonThumb({parent: @_e.actors_fav, vals: item}))
      )

  load_more_directors_fav:->
    @_e.more_directors_fav.place.hide()
    @_app.rest.users.persons.read(_opts.id, {type: "d"})
    .done(
      (data)=>
        if data && data.length
          for item in data
            i = 0
            while i < _directors.length && _directors[i].id != item.id
              i++
            if i >= _directors.length
              _directors.push(new PersonThumb({parent: @_e.directors_fav, vals: item}))
    )

  load_more_feed: ->
    @_e.more_feed.place.hide()
    _feed_page++;
    @_app.rest.users.feed.read(_opts.id, {per_page: 5, page: _feed_page})
      .done(
        (data) =>
          if data && data.length
            for item in data
              _feed.push(new FeedThumb({parent: @_e.feed, vals: item}))
            if data.length >=5
              @_e.more_feed.place.show()
      )

window.InitApp =  (opts = {}, page_name) ->
  new App(opts, page_name)
  delete window.InitApp