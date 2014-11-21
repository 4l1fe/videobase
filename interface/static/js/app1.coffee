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

scroll_to_obj = (obj, duration = 1000) ->
  $('html, body').stop().animate({scrollTop: obj.offset().top}, duration)

stars_tootltips = ["не смотреть", "хуже не бывает", "очень плохо", "плохо", "ниже среднего", "средне", "неплохо", "хорошо", "отлично", "великолепно", "лучше не бывает"]

class Player
  constructor: (@place, opts = {}) ->
    @current = undefined

  load: (loc, scroll = true, autoplay = true) ->
    if @current != undefined
      @clear()
    if (loc.price_type != 0 && loc.type != "playfamily")
      value = "&price=" + loc.price + "&view=" + encodeURI(loc.url_view)
    else
      value = ""
      if loc.value
        value = "&value=" + loc.value
      if loc.url_view
        value+= "&view=" + encodeURIComponent(loc.url_view)
    value+= "&autoplay=" + autoplay
    @place.empty().html('<iframe src="' + window.mi_conf.player_url + '?type=' + loc.type + value + '"></iframe>')
    if (scroll)
      scroll_to_obj @place

  clear: ->
    @place.addClass("player-empty")
    @place.empty().height("auto")
    @current = undefined

class PlayerCast
  constructor: (@place, opts = {}) ->
    @current = undefined

  load: (loc, scroll = true, autoplay = true) ->
    if @current != undefined
      @clear()
    if (loc.price_type != 0 && false)
      value = "&price=" + loc.price + "&view=" + encodeURI(loc.url_view)
    else
      value = ""
      if loc.value
        value = "&value=" + encodeURIComponent(loc.value || "")
      if loc.url_view
        value+= "&view=" + encodeURIComponent(loc.url_view)
    value+= "&autoplay=" + autoplay
    @place.empty().html('<iframe src="' + window.mi_conf.player_cast_url + '?type=' + loc.type + value + '"></iframe>')
    if (scroll)
      scroll_to_obj @place

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

  user_is_auth: (modal) ->
    return @_app.user_is_auth(modal)

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
        if opts.up
          @_place.prependTo(opts.parent)
        else
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
      ri = @elements["relation.rating"].self.rateit()
      ri
      .bind("beforerated beforereset", (event) =>
        if !@user_is_auth()
          event.preventDefault()
      )
      .bind "rated", (event) => @action_rate(ri.rateit("value"))
      .bind "reset", (event) => @toggle_notwatch()
      .bind "over", (event, value) -> $(this).attr('title', stars_tootltips[value]);
  ###
    @elements["poster"].self.css({"margin-left": -300}).load(->
      $this = $(this)
      $this.animate({"margin-left": 0}, 3000)
    )
  ###
  # @place().imagesLoaded()

  transform_attr: (attr, name, val) ->
    if attr == "href" && name == "id"
      return "/films/" + val + "/"
    else
      super

  transform_val: (name, val) ->
    if name == "releasedate"
      if val && typeof(val) == "string"
        return val.substr(0, 4)
      else
        return ''
    else
      super

  set_vals: (vals, do_not_set) ->
    if vals.title_alt == undefined
      vals.title_alt = vals.name
      if vals.name_orig && vals.name != vals.name_orig
        vals.title_alt+= " (" + vals.name_orig + ")"
      if vals.releasedate && typeof(val) == "string"
        vals.title_alt+= " " + vals.releasedate.substr(0,4)

    @elements["btn_price"].self.hide()
    if vals.locations && vals.locations.length
      vals.hasFree = false
      vals.price = 0
      price_loc_cnt = 0
      for loc in vals.locations
        loc.price = parseFloat(loc.price || 0)
        if loc.price_type == 0
          vals.hasFree = true
        else
          if loc.price && (vals.price == 0 || loc.price < vals.price)
            vals.price = loc.price
            vals.price_loc = loc.id
          price_loc_cnt++
      btn_cls = false
      btn_text = ""
      if !vals.hasFree && vals.price
        btn_cls = "btn-price"
        btn_text = "Смотреть<br><i>"
        btn_text+= "от " if price_loc_cnt > 1
        btn_text+= vals.price + " р. без рекламы</i>"
      else if vals.price
        @elements["btn_price"].self.css("display", "block")
        text = vals.price + " р. без рекламы"
        text = "от " + text if price_loc_cnt > 1
        @elements["price"].self.text(text)
      if !vals.price || vals.hasFree
        btn_cls = "btn-free"
        btn_text = "Смотреть<br/>бесплатно"
    else
      btn_cls = "btn-subscribe"
      btn_text = "Подписаться"
      @elements["btn"].self.click => @toggle_subscribe()
    if vals.relation && vals.relation.rating
      @elements["relation.rating"].self.rateit().rateit("value", vals.relation.rating)
    @elements["btn"].self.removeClass("btn-subscribe").removeClass("btn-price").removeClass("btn-free").addClass(btn_cls)
    @elements["btn_text"].self.html(btn_text).css("display", "block")
    super
    if !vals.hasFree && vals.price
      @elements["btn_text"].self.attr("href", @elements["btn_text"].self.attr("href") + "#" + vals.price_loc)
    else
      @elements["btn_text"].self.attr("href", @elements["btn_text"].self.attr("href") + "#player")
      if vals.price
        @elements["price"].self.parent().attr("href", @elements["price"].self.parent().attr("href") + "#" + vals.price_loc)

  action_rate: (val) ->
    @_app.film_action @vals.id, "rate", {
      rel: @vals.relation
      value: val
      callback: (new_state) =>
        # alert("done")
    }

  toggle_playlist: (status) ->
    @_app.film_action @vals.id, "playlist", {
      rel: @vals.relation
      state: status
      callback: (new_state) =>
        # alert("done")
    }
    if document.location.pathname.slice(0, 9) == "/playlist" && typeof(@_app.page().conf.film.id) == 'undefined'
      setTimeout(
        ()->
          document.location.reload(true)
        400
      )
    false

  toggle_notwatch: (status) ->
    @_app.film_action @vals.id, "notwatch", {
      rel: @vals.relation
      state: status
      callback: (new_state) =>
        # alert("done")
    }

  toggle_subscribe: (status) ->
    @_app.film_action @vals.id, "subscribe", {
      rel: @vals.relation
      state: status
      callback: (new_state) =>
        # alert("done")
    }
    false

  watchfilm: ->
    location.href = "/films/" + @vals.id + "/"

class CommentThumb extends Item
  constructor: (opts = {}, callback) ->
    @_name = "comment-thumb"
    if opts.vals
      @vals_orig = opts.vals
    super opts, =>
      if !opts.place
        $(".time-tape", @_place).data("miVal", @vals_orig.created)

  transform_attr: (attr, name, val) ->
    if attr == "href" && name == "user.id"
      return "/users/" + val + "/"
    super

  transform_val: (name, val) ->
    if name == "user.name"
      return val || "Пользователь"
    if name == "text"
      return val.replace(/\n+/gm, "<br/>")
    super

class PersonThumb extends Item
  constructor: (opts= {}, callback) ->
    @_name = "person-thumb"
    super

  transform_attr: (attr, name, val) ->
    if attr == "href" && name == "id"
      return "/persons/" + val + "/"
    else
      super

class FeedThumb extends Item
  constructor: (opts = {}, callback) ->
    @_name = "feed-thumb"
    if opts.vals
      @_type = opts.vals.type
      @vals_orig = opts.vals
    super opts, =>
      if !opts.place
        $(".tape-" + @_type, @_place).removeClass("tape-thumb")
        $(".tape-thumb", @_place).remove()
        $(".time-tape", @_place).data("miVal", @vals_orig.created)
        @_place.removeClass("display-none")
        if @_type == "film-r"
          @elements["object.rating"].self.rateit().rateit("value", opts.vals.object.rating)

  transform_val: (name, val) ->
    if name == "user.name"
      return val || "Пользователь"
    else if @_type == "film-c" && name == "object.text"
      return val.replace(/\n+/gm, "<br/>")
    super

  transform_attr: (attr, name, val) ->
    type = @_type
    if type.substr(0,4) == "film"
      if name == "object.id" || name == 'object.film.id' && attr="href"
        return "/films/" + val + "/"
      if name == "object.name"
        return val + " (" + @vals_orig.object.releasedate.substr(0,4) + ")"
    if type.substr(0,4) == "pers" && attr="href"
      if name == "object.id"
        return "/persons/" + val + "/"
      else if name == "object.film.id"
        return "/films/" + val + "/"
    if type.substr(0,4) == "user" && attr="href"
      if name == "object.id"
        return "/users/" + val + "/"
    if name == "user.id" && attr="href"
      return "/users/" + val + "/"
    if name == "created"
      try
        return time_text(new Date(val))
      catch
        return val
    super

class CastThumb extends Item
  constructor: (opts = {}, callback) ->
    @_name = "cast-thumb"
    if opts.vals
      @_type = opts.vals.type
      @vals_orig = opts.vals
      opts.vals.start_date = new Date(opts.vals.start)
      opts.vals.min_vs_start = opts.vals.min_vs_start = Math.floor((new Date() - opts.vals.start_date) / 60 / 1000)
      opts.vals.duration = opts.vals.duration || 180
      opts.vals.is_online = opts.vals.min_vs_start >=0 && opts.vals.min_vs_start < opts.vals.duration

    super opts, =>
      if (!opts.place)
        label_prim_str = ''
        label_prim_cls = 'label-primary'
        label_fright_str = ''
        label_fright_cls = ''
        if @vals.is_online
          label_prim_str = "Онлайн"
          label_prim_cls = 'label-success'
          @elements["btn"].self.show().addClass("btn-free").html("Смотреть<br/>бесплатно")
        else if @vals.min_vs_start < 0
          if @vals.min_vs_start > -1440
            label_prim_str = ''
            if @vals.min_vs_start > -60
              label_prim_str = "примерно "
            label_prim_str += 'через ' + duration_text( -@vals.min_vs_start )
          else
            label_prim_str = time_text(@vals.start_date)
          @elements["btn"].self.show().addClass("btn-subscribe").text("Подписаться")
          @elements["btn"].self.click @action_subscribe
        else
          label_fright_str = time_text(@vals.start_date)
          label_fright_cls = 'cast-archive-date'
          label_prim_str = 'Архив'
        @elements["label_prim"].self.removeClass("label-primary").addClass(label_prim_cls).text(label_prim_str)
        @elements["label_fright"].self.addClass(label_fright_cls).text(label_fright_str)

  transform_attr: (attr, name, val) ->
    if attr == "href" && name == "id"
      return "/casts/" + val + "/"
    else
      super

  transform_val: (name,val) ->
    if name == "pg_rating"
      return val?" (" + val + ")":""
    super

  action_subscribe: =>
    @_app.cast_action( @vals.id, "subscribe" )
    return false

class Deck
  constructor: (@_place, opts = {}) ->
    @load_counter = 0
    @page = 0
    @load_func = undefined
    @items = []
    @more = {}
    @save_footer = false

    self = @
    $("." + @element_name, @_place).each(
      ->
        self.add_item_DOM($(this))
    )
    @load_func = opts.load_func if opts.load_func
    if opts.more_place
      @load_more_bind(opts.more_place)

  onchange: ->

  add_item_DOM: (obj) ->
    @items.push(new @item_class({place: obj, do_not_set: true}))
    @onchange()

  add_item: (item, onchange_call = true, up = false) ->
    @items.push(new @item_class({parent: @_place, vals: item, up: up}))
    if onchange_call
      @onchange()

  add_items: (items) ->
    for item in items
      @add_item(item, false)
    if @save_footer
      @save_footer = false
      @_place.removeClass("loading").css("min-height", 0)
    @onchange()

  get_items: ->
    @items

  load_more_bind: (place) ->
    @more.place = place
    @more.btn = $("a", place)
    @more.btn.click(=> @load_more(); return false)

  load_more: (opts) ->
    if @load_func != undefined
      @load_counter++
      @load_func(@, opts)

  load_more_hide: (loading = true) ->
    if loading
      @more.place.addClass("add-filter-loading")
    else
      @more.place.hide() if @more.place

  load_more_show: ->
     @more.place.removeClass("add-filter-loading").show() if @more.place

  clear: (loading_more = true) ->
    @load_counter++
    if loading_more
      pTop = @_place.offset().top
      wScrollTop = $(window).scrollTop()
      wH = $(window).height()
      pH = @_place.height()
      if (pTop - wScrollTop + pH) >= wH
        @save_footer = true
        @_place.css("min-height", wH - pTop + wScrollTop).addClass("loading")
    for item in @items
      item.remove()
    @items = []
    @_place.empty()
    @page = 0
    @onchange(true)

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
    $(".time-tape", @_place).each ->
      $this = $(this)
      if $this._failed
        return
      if !$this._datetime
        try
          $this._datetime = new Date($this.data("miVal"))
        catch
          $this._failed = true
          return
      $this.text(time_text($this._datetime))

  onchange: ->
    @time_update()

class FeedDeck extends Deck
  constructor: (place, opts = {}) ->
    @element_name = "feed-thumb"
    @item_class = FeedThumb
    super
    setInterval(
      =>
        @time_update()
    , 1000
    )
    @time_update()

  time_update: ->
    $(".time-tape", @_place).each ->
      $this = $(this)
      if $this._failed
        return
      if !$this._datetime
        try
          $this._datetime = new Date($this.data("miVal"))
        catch
          $this._failed = true
          return
      $this.text(time_text($this._datetime))

    return
    #for item in @items
    #  if item.elements.time_text.val
    #    item.elements.time_text.self.text(time_text(new Date(item.elements.time_text.val)))


class FilmsDeck extends Deck
  constructor: (place, opts = {}) ->
    @element_name = "film-thumb"
    @item_class = FilmThumb
    super
    $(window).resize(=> @onchange())

  onchange: (global = false) ->
    body_width = $("body").width()
    # items_inrow = Math.floor($("body").width() / 250)
    if body_width > 991
      items_inrow = 4
    else if body_width > 767
      items_inrow = 3
    else
      items_inrow = 2

    if @current_items_inrow != items_inrow
      global = true
    @current_items_inrow = items_inrow
    if global == true
      $("hr", @_place).remove();

    for i in [0...@items.length-1]
      if ((i + 1) % items_inrow == 0)
        el = @items[i].place()
        if !el.next().is("hr")
          $("<hr />").insertAfter(el)

class CastsDeck extends Deck
  constructor: (place, opts = {}) ->
    @element_name = "cast-thumb"
    @item_class = CastThumb
    super
    $(window).resize(=> @onchange())

  onchange: (global = false) ->
    body_width = $("body").width()
    # items_inrow = Math.floor($("body").width() / 250)
    if body_width > 991
      items_inrow = 4
    else if body_width > 767
      items_inrow = 3
    else
      items_inrow = 2

    if @current_items_inrow != items_inrow
      global = true
    @current_items_inrow = items_inrow
    if global == true
      $("hr", @_place).remove();

    for i in [0...@items.length-1]
      if ((i + 1) % items_inrow == 0)
        el = @items[i].place()
        if !el.next().is("hr")
          $("<hr />").insertAfter(el)

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

  constructor: (opts = {}, name = "Simple") ->
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
    @rest.films.add("comments")
    @rest.films.add("action", {isSingle: true})
    @rest.films.action.add("rate")
    @rest.films.action.add("subscribe")
    @rest.films.action.add("notwatch")
    @rest.films.action.add("playlist")
    @rest.films.action.add("comment")
    @rest.add("persons")
    @rest.persons.add("filmography", {isSingle: true})
    @rest.persons.add("action", {isSingle: true})
    @rest.persons.action.add("subscribe")
    @rest.add("casts")
    @rest.add("castschats")
    @rest.castschats.add("msgs")
    @rest.castschats.add("send")
    @rest.casts.add("list")
    @rest.casts.add("subscribe")

    @_e =
      search:
        frm: $("#frm_search")
    @_e.search.input = $(".inp-search", @_e.search.frm)
    @_e.search.btn = $(".btn-search", @_e.search.frm)
    q = @query_params("q")
    @_e.search.input.val(q) if q

    @auth_modal = $("#reg_enter")

    if name != undefined
      @show_page(name, conf.page_conf)

    $("#login_btn").click (e)=>
      e.preventDefault()
      e.stopPropagation()
      @show_modal("login")

    $("#reg_btn").click (e) =>
      e.preventDefault()
      e.stopPropagation()
      @show_modal("reg")

    current_url = window.location.href.toString().split(window.location.host)[1]
    $("form", @auth_modal).each ->
      $this = $(this)
      action = $this.attr("action")
      if /\?/.test(action)
        action+= "&"
      else
        action+= "?"
      $this.attr("action", action + "back_url=" + encodeURIComponent(current_url))

    $("a", $(".soc-hor", @auth_modal)).each ->
      $this = $(this)
      href = $this.attr("href")
      if /\?/.test(href)
        href+= "&"
      else
        href+= "?"
      $this.attr("href", href + "next=" + encodeURIComponent("/tokenize/?back_url=" + current_url))


  show_modal: (index) ->
    index = "reg" if index == undefined
    if index == "reg"
      $('.popup-tabs-a >li, .popup-content > div', @auth_modal).removeClass('active');
      $('.popup-tabs-a >li:eq(0), .popup-content > div:eq(0)', @auth_modal).addClass('active');
    else
      $('.popup-tabs-a >li, .popup-content > div').removeClass('active');
      $('.popup-tabs-a >li:eq(1), .popup-content > div:eq(1)', @auth_modal).addClass('active');
    @auth_modal.modal("show")

  user_action: (id, action, opts = {}) ->
    if @user_is_auth()
      rel = opts.rel || {}
      action_str = action
      if action_str == "friendship"
        new_state = state_toggle(opts.status, rel[action_str])
        if new_state
          doit = "update"
        else
          doit = "destroy"
        @rest.users.action[action][doit](id)
        .done(
          ->
            rel[action_str] = new_state if opts.rel
            opts.callback(new_state) if opts.callback
        )

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
      else if action == "comment"
        @rest.films.action.comment.update id, {text: opts.text}
            .done(
              ->
                opts.callback(true) if opts.callback
            )
            .fail(
              ->
                opts.callback(false) if opts.callback
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

  cast_action: (id, action, opts = {}) ->
    if( @user_is_auth() )
      if( action == "subscribe" )
        @rest.casts.subscribe.create(id)

  config: (name) ->
    if name == undefined
      return conf
    else
      return conf[name]

  user_is_auth: (ask_sign_in = true) ->
    if !@rest.has_auth()
      if ask_sign_in
        @auth_modal.modal("show")
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
      error "No page " + name + " found"

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
#      error "Unable to init page " + name, "crit"
#      return undefined

class Page_Simple extends Page


class Page_Search extends Page
  films = undefined
  self = undefined
  constructor: (@conf)->
    super
    self = @
    @_app.get_tpl("film-thumb")
    films_deck = new FilmsDeck($("#films"), {load_func: @load_more_films})
    films_deck.page = 1
    films_deck.load_more_bind($("#films_more"))

  load_more_films: (deck, opts = {}) ->
    deck.load_more_hide()
    params = {text: self.conf.search_text || "", page: deck.page + 1}
    current_counter = deck.load_counter
    self._app.rest.films.read("search", params)
    .done(
      (data) =>
        return if current_counter != deck.load_counter
        if data.items
          deck.add_items(data.items)
          if data.items.length >= 12
            deck.load_more_show(false)
          else
            deck.load_more_hide(false)
          deck.page = data.page
        opts.callback() if opts.callback
    )
    .fail(
      (data) =>
    )

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
    films_deck = new FilmsDeck($("#films"), {load_func: (deck) => @load_more_films(deck)})
    films_deck.load_more_bind($("#films_more"))
    $(".film-thumb", $("#films_new")).each(
      ->
        new FilmThumb({place: $(this), do_not_set: true})
    )
    @_e.filter =
        genre: $("#filter_genres")
        year_old: $("#filter_year_old")
        rating: $("#filter_rating")
        price: $("#filter_price")
        sort: $("#filter_sort")

    params = @_app.query_params()
    params["price"] = (params["price"] || "") + "|"
    params["price"]+= params["instock"] if params["instock"]

    $.each(@_e.filter, (index) ->
      el = this
      el._title = $(".sprite > span", el)
      el._selected = undefined
      el._options = []
      $(".dropdown-menu a", el).each( ->
        $this = $(this)
        $this._val = $this.data("miId")
        $this._text = $this.text()
        el._options.push($this)
        $this.click( ->
          if el._selected != $this
            el._selected = $this
            el._title.text($this._text)
            self.filter_changed()
          el.removeClass("open")
          return false
        )
        if params[index] && ($this._val == undefined || (params[index].toString() == $this._val.toString()))
          el._selected = $this
          el._title.text($this._text)
      )
      if el._selected == undefined
        el._selected = el._options[0]
        el._title.text(el._options[0]._text)
    )
    @update_filter_params(false)
    if (films_deck.get_items().length >= 12)
      @load_more_films(films_deck, {page: 2})
    else
      films_deck.load_more_hide(false)
    $('.crsl-items').carousel({itemMinWidth: 200, itemEqualHeight: true, visible: 3});

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
    query_string=""

    for key, el of @_e.filter
      val = el._selected._val
      if key == "price"
        vals = val.split("|")
        if vals[0] || vals[0] == "0"
          _filter_params["price"] = vals[0]
          query_string+= "&" if query_string
          query_string+= "price=" + vals[0]
        else
          _filter_params["price"] = null
        if vals[1] || vals[1] == "0"
          _filter_params["instock"] = vals[1]
          query_string+= "&" if query_string
          query_string+= "instock=" + vals[1]
        else
          _filter_params["instock"] = null
      else
        if val && val != "0"
          _filter_params[key] = val
          query_string+= "&" if query_string
          query_string+= key + "=" + val
        else
          _filter_params[key] = null

    page = films_deck.page || 1
    _filter_params.page = page
    #query_string+= "&" if query_string
    more_btn_href = "/?" + query_string + "page=" + (page+1)
    #query_string+= "page=" + films_deck.page

    query_string = "?" + query_string if query_string
    if update_href
      if history && history.pushState
        history.pushState null, null, query_string
      $("a", $("#films_more")).attr("href", more_btn_href)

  load_more_films: (deck, opts = {}) ->
    deck.load_more_hide()
    params = $.extend(_filter_params, opts.params || {})
    params["recommend"] = 1 if @user_is_auth(false)
    if opts.clear_output
      deck.clear(false)
      params.page = 1
    else
      params.page = opts.page || (deck.page + 1)
    current_counter = deck.load_counter
    self._app.rest.films.read("search", params)
    .done(
      (data) =>
        return if current_counter != deck.load_counter
        if data.items
          deck.add_items(data.items)
          if data.items.length >= 12
            deck.load_more_show()
          else
            deck.load_more_hide(false)
          deck.page = data.page
          if opts.clear_output
            scroll_to_obj $("#filter_content")
        else
          deck.load_more_hide(false)
        @update_filter_params()
        opts.callback() if opts.callback
    )
    .fail(
      (data) =>
        deck.load_more_hide(false)
    )

# implementing Login and Register Page class
class Page_Login extends Page

class Page_Register extends Page
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
    comments_deck = new CommentsDeck($("#comments"), {load_func: => @load_more_comments()})
    comments_deck.load_more_bind($("#comments_more"))
    actors_deck = new PersonsDeck($("#actors"), {load_func: => @load_all_actors()})
    actors_deck.load_more_bind($("#actors_more"))

    @_e.rateit = $("#rateit")
    @_e.rateit
    .bind("beforerated beforereset", (event) =>
      if !@user_is_auth()
        event.preventDefault()
    )
    .bind "rated", (event) => @action_rate(@_e.rateit.rateit("value"))
    .bind "reset", (event) => @action_notwatch_toggle()
    .bind "over", (event, value) -> $(this).attr('title', stars_tootltips[value]);

    if @conf.relation && @conf.relation.rating
      @_e.rateit.rateit "value", @conf.relation.rating

    @_e.playlist_btn = $("#playlist_btn")
    @_e.playlist_btn.bind("click", => @action_playlist_toggle()) if @_e.playlist_btn.length
    @_e.subscribe_btn = $("#subscribe_btn")
    @_e.subscribe_btn.bind("click", => @action_subscribe_toggle()) if @_e.subscribe_btn.length

    @_e.add_comment = {}
    @_e.add_comment.place = $("#add_comment")
    @_e.add_comment.submit_btn = $("input[type=submit]", @_e.add_comment.place)
    @_e.add_comment.textarea_wrapper = $("#comment_textarea_wrapper")
    @_e.add_comment.textarea_error = $("p", @_e.add_comment.textarea_wrapper)

    if @_e.add_comment.submit_btn.size()
      $("form", @_e.add_comment.place).submit( => @add_comment(); return false)
      @_e.add_comment.text = $("textarea", @_e.add_comment.place)
    else
      $(".login", @_e.add_comment.place).click(=> @_app.show_modal("login"); return false)
      $(".register", @_e.add_comment.place).click(=> @_app.show_modal("reg"); return false)

    self = @
    if @conf.locations && @conf.locations.length
      if @conf.locations.length > 1
        $(".location-thumb", $("#locations")).each( ->
          $this = $(this)
          id = $this.data("miVal")
          i = 0
          loc = undefined
          while i < self.conf.locations.length && self.conf.locations[i].id != id
            i++
          loc = self.conf.locations[i] if i < self.conf.locations.length
          if loc
            if (loc.price)
              loc.price = Math.ceil(loc.price)
            $this.click(-> self.play_location(id))
            locations[id] = loc
        )
      else
        locations[@conf.locations[0].id] = @conf.locations[0]

      @player = new Player($("#frame_player"))
      @player.clear()

      loc_id = window.location.hash.substr(1);
      if locations[loc_id] == undefined
        loc_id = undefined
        loc_price = false
        loc_price_id = false
        for key,item of locations
          if item.price_type == 0
            loc_id = key if !loc_id
          else
            if item.type == "playfamily" || loc_price_id == false || loc_price == false || loc_price > item.price
              loc_price_id = item.id
              loc_price = item.price
              if item.type == "playfamily"
                loc_price = 1
      if !loc_id
        loc_id = loc_price_id
      @play_location(loc_id, false) if loc_id

  load_more_comments: ->
    comments_deck.load_more_hide()
    @_app.rest.films.comments.read(@conf.id, {page: (comments_deck.page || 1) + 1})
    .done(
      (data) ->
        total_page_count = Math.ceil(data.total_cnt/data.ipp)
        if data && data.items
          comments_deck.add_items(data.items)
          comments_deck.time_update()
          comments_deck.page = data.page
          if data.page < total_page_count
            comments_deck.load_more_show()
          else
            comments_deck.load_more_hide(false)
        else
          comments_deck.load_more_hide(false)
    )
    .fail(
      ->
        comments_deck.load_more_hide(false)
    )

  add_comment: ->
    text = @_e.add_comment.text.val()
    @_e.add_comment.textarea_wrapper.removeClass("has-error")
    @_e.add_comment.textarea_error.text("")
    error = false
    if text == ""
      error = "Введите, пожалуйста, текст комментария."
    else if text.length < 20
      error = "Количество букв в тексте не должно быть меньше 20."
    else if text.length > 8000
      error = "Количество букв в тексте не должно превышать 8000."
    else
      @_e.add_comment.text.attr("disabled", "disabled")
      @_e.add_comment.submit_btn.attr("disabled", "disabled")
      @_app.film_action(@conf.id, "comment", {
        text: text,
        callback: (result) =>
          @_e.add_comment.text.removeAttr("disabled")
          @_e.add_comment.submit_btn.removeAttr("disabled")
          if result
            @_e.add_comment.text.val("")
            @_app.rest.films.comments.read @conf.id, {per_page: 1, page: 1}
              .done(
                (res) =>
                  if res.items && res.items.length
                    $("#has_comments").show()
                    comments_deck.add_item(res.items[0], true, true)
              )
              .fail(
                (res) =>
                  error = "Не удалось сохранить комментарий."
                  if res.error && res.error.text
                    error = res.error.text
                  @_e.add_comment.textarea_wrapper.addClass("has-error")
                  @_e.add_comment.textarea_error.text(error)
                  @_e.add_comment.text.focus()
              )
      })
    if error
      @_e.add_comment.textarea_wrapper.addClass("has-error")
      @_e.add_comment.textarea_error.text(error)
      @_e.add_comment.text.focus()


  play_location: (id, scroll = false) ->
    @player.load(locations[id], scroll) if locations[id]

  load_all_actors: () ->
    actors_deck.load_more_hide(false);
    @_app.rest.films.persons.read(@conf.id, {type: "a", top: actors_deck.get_items().length})
    .done(
      (data)=>
        if data && data.length
          actors_deck.add_items(data)
    )
    actors_deck._place.appendTo($("#actors_full").removeClass("hide"))
    $("#actors_left").hide();
    $("#toggle_col").removeClass("col-md-9")

  action_rate: (val) ->
    @_app.film_action @conf.id, "rate", {
      rel: @conf.relation
      value: val
      callback: (new_value) =>
        # alert("done")
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
    false

  action_playlist_toggle: (status) ->
    @_app.film_action(@conf.id, "playlist", {
      state: status
      rel: @conf.relation
      callback: =>
    })
    false

class Page_Person extends Page
  films_deck = undefined
  constructor: (@conf) ->
    super
    @_app.get_tpl("film-thumb")
    films_deck = new FilmsDeck($("#films"), {load_func: (deck) =>@load_more_films(deck) })
    films_deck.load_more_bind($("#films_more"))
    films_deck.page = 1
    @_e.subscribe_btn = $("#subscribe").click(=> @action_subscribe())

  action_subscribe: (status) ->
    @_app.person_action(@conf.id, "subscribe", {
      rel: @conf.relation
      status: status
      callback: =>
        # alert("done")
    })
    false

  load_more_films: (deck) ->
    current_counter = deck.load_counter
    deck.load_more_hide()
    @_app.rest.persons.filmography.read(@conf.id, {page: deck.page + 1})
    .done(
      (data) =>
        return if current_counter != deck.load_counter
        if data.items
          deck.add_items(data.items)
          if data.items.length >= 12
            deck.load_more_show()
            deck.page = data.page
          else
            deck.load_more_hide(false)
        else
          deck.load_more_hide(false)
    )
    .fail(
      (data) =>
        deck.load_more_hide(false)
    )

class Page_Playlist extends Page
  constructor: (@conf) ->
    super
    film_page = new Page_Film(@conf.film)
    $('.toggle-playlist').click (e)->
      e.preventDefault();
      $(this).toggleClass('active')
      $('.tp').slideToggle 'slow', ->
        if $(this).is(':visible')
          $('.toggle-playlist span').text('Скрыть плейлист')
        else
          $('.toggle-playlist span').text('Показать плейлист');
    $("#playlistof_btn").bind("click", =>
      @_app.film_action(@conf.film.id, "playlist", {
          status: false
          rel: @conf.relation
          callback: =>
            if @conf.next && @conf.next.id
              location.href = "/playlist/" + @conf.id + "/"
            else if @conf.previous && @conf.previous.id
              location.href = "/playlist/" + @conf.previous.id + "/"
            else
              location.href = "/playlist/"
      })
      return false
    )
    $('.crsl-items').carousel({itemMinWidth: 155, itemEqualHeight: true, visible: 6});
    @_app.get_tpl("person-thumb")

class Page_Feed extends Page
  feed_deck = undefined
  constructor: (@conf) ->
    super
    feed_deck = new FeedDeck($("#feed"), {load_func: (deck) =>@load_more_feed(deck) })
    feed_deck.load_more_bind($("#feed_more"))
    feed_deck.page = 1
    @_app.get_tpl("feed-thumb")

  load_more_feed: (deck) ->
    current_counter = deck.load_counter
    deck.load_more_hide()
    @_app.rest.users.feed.read(@conf.user_id, {page: deck.page + 1})
    .done(
      (data) =>
        return if current_counter != deck.load_counter
        if data.items
          deck.add_items(data.items)
          if data.items.length >= 10
            deck.load_more_show()
            deck.page = data.page
          else
            deck.load_more_hide(false)
        else
          deck.load_more_hide(false)
    )
    .fail(
      (data) =>
        deck.load_more_hide(false)
    )

class Page_Account extends Page
  self: undefined
  constructor: () ->
    super
    $('.checkbox-default').uniform()
    $('.radio-default').uniform({radioClass: 'radio-class'})

    @_e.pvt_selector = $("#pvt_selector")
    self = @

    $("input:radio", @_e.pvt_selector).click ->
      $this = $(this)
      if self._e.pvt_selector.active
        val = $this.val()
        self._e.pvt_selector.obj.text($(".value" + val, self._e.pvt_selector).text())
        $("input").filter("[name=" + self._e.pvt_selector.active + "]").val(val)

    $("a", $("#pvt_list")).click (e) ->
      e.preventDefault()
      self.pvt_select_toggle($(this))

  pvt_select_toggle: ($this) ->
    name = $("input", $this.parent()).attr("name")
    if @_e.pvt_selector.active == name
      @_e.pvt_selector.hide()
      @_e.pvt_selector.active = undefined
    else
      @_e.pvt_selector.insertAfter($this).show()
      @_e.pvt_selector.active = name
      @_e.pvt_selector.obj = $this
      val = $("input", $this.parent()).val()
      $("input:radio", @_e.pvt_selector).each ->
        $this = $(this)
        $.uniform.update($this.prop('checked', $this.val() == val))

class Page_User extends Page
  films_deck = undefined
  feed_deck = undefined
  constructor: (@conf) ->
    super
    films_deck = new FilmsDeck($("#films"), {load_func: (deck) =>@load_more_films(deck) })
    films_deck.load_more_bind($("#films_more"))
    films_deck.page = 1
    @_e.friendship_btn = $("#friendship").click(=> @action_friendship())
    feed_deck = new FeedDeck($("#feed"), {load_func: (deck) =>@load_more_feed(deck) })
    feed_deck.load_more_bind($("#feed_more"))
    feed_deck.page = 1
    @_app.get_tpl("feed-thumb")
    @_app.get_tpl("film-thumb")

  action_friendship: (status) ->
    @_app.user_action(@conf.id, "friendship", {
      rel: @conf.relation
      status: status
      callback: =>
        # alert("done")
    })
    false

  load_more_films: (deck) ->
    current_counter = deck.load_counter
    deck.load_more_hide()
    @_app.rest.users.films.read(@conf.id, {page: deck.page + 1})
    .done(
      (data) =>
        return if current_counter != deck.load_counter
        if data.items
          deck.add_items(data.items)
          if data.items.length >= 12
            deck.load_more_show()
            deck.page = data.page
          else deck.load_more_hide(false)
        else deck.load_more_hide(false)
    )
    .fail(
      (data) =>
        deck.load_more_hide(false)
    )

  load_more_feed: (deck) ->
    current_counter = deck.load_counter
    deck.load_more_hide()
    @_app.rest.users.feed.read(@conf.id, {page: deck.page + 1})
    .done(
      (data) =>
        return if current_counter != deck.load_counter
        if data.items
          deck.add_items(data.items)
          if data.items.length >= 10
            deck.load_more_show()
            deck.page = data.page
          else
            deck.load_more_hide(false)
        else
          deck.load_more_hide(false)
    )
    .fail(
      (data) =>
        deck.load_more_hide(false)
    )

class Page_CastsList extends Page
  casts_deck = undefined
  self = undefined
  _filter_params = {}
  _filter_counter = 0

  constructor: () ->
    self = @
    super
    casts_deck = new CastsDeck($("#casts"), {load_func: (deck) =>@load_more_casts(deck) })
    casts_deck.page = 1
    casts_deck.load_more_hide(false)
    casts_deck.load_more_bind($("#casts_more"))

    @_e.filter =
      status: $("#filter_cast_status")
      tag: $("#filter_cast_tag")
      quality: $("#filter_cast_quality")
      price_high: $("#filter_cast_price")

    params = @_app.query_params()

    $.each(@_e.filter, (index) ->
      el = this
      el._title = $(".sprite > span", el)
      el._selected = undefined
      el._options = []
      $(".dropdown-menu a", el).each( ->
        $this = $(this)
        $this._val = $this.data("miId")
        $this._text = $this.text()
        el._options.push($this)
        $this.click( ->
          if el._selected != $this
            el._selected = $this
            el._title.text($this._text)
            self.filter_changed()
          el.removeClass("open")
          return false
        )
        if params[index] && ($this._val == undefined || (params[index].toString() == $this._val.toString()))
          el._selected = $this
          el._title.text($this._text)
      )
      if el._selected == undefined
        el._selected = el._options[0]
        el._title.text(el._options[0]._text)
    )
    @update_filter_params(false)

  filter_changed: () ->
    _filter_counter++
    current_filter_counter = _filter_counter
    setTimeout(
      =>
        if _filter_counter == current_filter_counter
          @update_filter_params()
          opts =
            clear_output: true
            page_loading: false
            params: _filter_params
          @load_more_casts(casts_deck, opts)
      @_app.config("filter_delay")
    )

  load_more_casts: (deck, opts = {}) ->
    deck.load_more_hide()
    params = $.extend(_filter_params, opts.params || {})
    if opts.clear_output
      deck.clear(true)
      params.page = 1
    else
      params.page = opts.page || (deck.page + 1)
    current_counter = deck.load_counter

    self._app.rest.casts.read("list", params)
    .done(
      (data) =>
        return if current_counter != deck.load_counter
        if data.items
          deck.add_items(data.items)
          if data.items.length >= 12
            deck.load_more_show()
          else
            deck.load_more_hide(false)
          deck.page = data.page
          if opts.clear_output
            scroll_to_obj $("#filter_content")
        else
          deck.load_more_hide(false)
        @update_filter_params()
        opts.callback() if opts.callback
    )
    .fail(
      (data) =>
        deck.load_more_hide(false)
    )

  update_filter_params: (update_href = true) ->
    query_string=""
    for key, el of @_e.filter
      val = el._selected._val
      if val && val != "0"
        _filter_params[key] = val
        query_string+= "&" if query_string
        query_string+= key + "=" + val
      else
        _filter_params[key] = null

    page = casts_deck.page || 1
    _filter_params.page = page
    more_btn_href = "/?" + query_string + "page=" + (page+1)

    query_string = "?" + query_string if query_string
    if update_href
      if history && history.pushState
        history.pushState null, null, query_string
      $("a", $("#casts_more")).attr("href", more_btn_href)

class Page_Cast extends Page
  constructor: (@conf) ->
    super
    @chat =
      active: true
      last_id: 0
      guests: 0
      counter: 0
      attempts: [0,0,0]
      timeout: [2, 5, 10]
      attempts_pos: 0

    @_e =
      cast_subscribe_btn: $('#cast_subscribe_btn')
      player:
        wrapper: $("#player_wrapper")
        frame: $("#player_frame")
      chat:
        wrapper: $("#chat_wrapper")
        list: $("#chat_list")
        input: $("#chat_input")
        ico: $("#chat_ico")
      time_counter: $("#time_counter")
      guests_cnt: $("#guests_cnt")
    @conf.start_date = new Date(@conf.start)
    @conf.duration = @conf.duration || 180
    @conf.min_vs_start = Math.floor((new Date() - @conf.start_date) / 60 / 1000)
    @conf.is_online = @conf.min_vs_start >=0 && @conf.min_vs_start < @conf.duration
    self = @
    @_e.cast_subscribe_btn.click @action_cast_subscribe
    if @conf.is_online
      @player = new PlayerCast(@_e.player.frame)
      if @conf.locations && @conf.locations.length
        @player.load(@conf.locations[0])
      @_e.chat.ico.click(-> self.toggle_chat())
      @_e.chat.input
        .keypress((e) -> self.sendmsg_chat() if e.which == 13)
        .focus( -> return false if !self.user_is_auth())
      @update_chat()
    else if @conf.min_vs_start < 0 && @_e.time_counter.length
      @timer_tick()

    casts_deck = new CastsDeck($("#casts"))

  timer_tick: () ->
    min_left = Math.floor((new Date() - @conf.start_date) / 60 / 1000)
    if min_left >=0 || (@conf.min_vs_start < -40 && min_left >= -40)
      location.reload()
    else
      @_e.time_counter.text(duration_text(-min_left))
      func = => @timer_tick()
      setTimeout func, 10000

  sendmsg_chat: () ->
    if @_app.user_is_auth()
      text = @_e.chat.input.val()
      if text.length < 2
        return
      @_e.chat.input.prop('disabled', true);
      @_app.rest.castschats.send.create(@conf.id, {text: text})
        .done(
          =>
            @update_chat(undefined, => @_e.chat.input.val("").prop('disabled', false))
        )
        .fail(
        )

  update_chat: (limit, cb) ->
    if !@conf.is_online
      return
    @chat.counter++
    local_counter = @chat.counter
    limit = limit || 20
    @_app.rest.castschats.msgs.read @conf.id, {id_low: (@chat.last_id|| -1) + 1, limit: limit}
      .done(
        (data)=>
          if local_counter == @chat.counter
            if data && data.length
              i = data.length - 1
              while i >= 0
                name = "пользователь"
                if data[i].user
                  name = data[i].user.name
                text = data[i].text || "&nbsp;"
                e = $('<div class="cast-chat-item"><div class="cast-chat-item-body"><span class="cast-chat-item-username">' + name + '</span>: <span class="cast-chat-item-msg">' + text + '</span></div></div>').appendTo(@_e.chat.list)
                i--
              @_e.chat.list.animate({ scrollTop: e.position().top}, "slow");
              if data.length >= limit
                @chat.attempts = [0,0,0]
                @chat.attempts_pos = 0
              else
                if @chat.attempts_pos == 0
                  @chat.attempts[0]++
                  if @chat.attempts[0] > 10
                    @chat.attempts_pos = 1
                    @chat.attempts[0] = 0
              @chat.last_id = data[data.length-1].id || @chat.last_id
            else
              if @chat.attempts_pos < 2
                @chat.attempts[@chat.attempts_pos]++
                if @chat.attempts[@chat.attempts_pos] > 10
                  @chat.attempts[@chat.attempts_pos] = 0
                  @chat.attempts_pos++
            if !@chat.active
              @chat.attempts_pos = 2
              @chat.attempts = [0,0,0]
            @update_chat_set(@chat.attempts_pos)
        cb(true) if typeof cb == "function"
      )
      .fail(
        =>
          if local_counter == @chat.counter
            @chat.attempts = [0,0,0]
            @chat.attempts_pos = 0
            @update_chat_set(2)
          cb(false) if typeof cb == "function"
      )

  update_chat_set: (timeout_id) ->
    func = => @update_chat()
    setTimeout func, (@chat.timeout[timeout_id] || @chat.timeout[2])*1000


  toggle_chat: (active) ->
    active = !@chat.active if active == undefined
    return if @chat.active == active
    if active
      @chat.active = true
      @update_chat()
      @_e.player.wrapper.addClass("col-md-8")
      @_e.chat.wrapper.show()
    else
      @chat.active = false
      @_e.chat.wrapper.hide()
      @_e.player.wrapper.removeClass("col-md-8")
    false

  action_cast_subscribe: =>
    @_app.cast_action( @_app.page().conf.id, "subscribe" )
    return false

window.InitApp =  (opts = {}, page_name) ->
  new App(opts, page_name)
  delete window.InitApp