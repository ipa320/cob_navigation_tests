define [ 'backbone', 'templates/textFilterRow', 'chosen' ], ( Backbone, textFilterRowTmpl, chosen )->
  Backbone.View.extend
    tagName: 'div'
    className: 'textFilterRow'
    events:
      'change':     'change'
      'keyup':      'keyup'
      'click .and': 'andClicked'
      'click .or':  'orClicked'

    initialize: ->
      @listenTo @model, 'change:link', @linkChanged

    render: ->
      @$el.html textFilterRowTmpl()
      this

    keyup: ( e )->
      if e.keyCode == 27 # escape
        @trigger 'escape'
      if e.keyCode == 13 # enter
        do @andClicked
      do @change

    change: ->
      @model.set 'field', @$( '.filterField' ).val()
      @model.set 'type',  @$( '.filterType'  ).val()
      @model.set 'value', $.trim( @$( '.filterValue' ).val())

    andClicked: ->
      @trigger 'andClicked'
      do @setAndLink

    orClicked: ->
      @trigger 'orClicked'
      do @setOrLink

    setAndLink: ->
      @$( '.and, .or' ).hide()
      @$( '.link' ).text 'and'
      @model.set 'link', 'and'

    setOrLink: ->
      @$( '.and, .or' ).hide()
      @$( '.link' ).text 'or'
      @model.set 'link', 'or'

    linkChanged: ->
      link = @model.get 'link'
      if !link
        @$( '.and, .or' ).show()
        @$( '.link' ).text ''
      else
        @$( '.and, .or' ).hide()
        @$( '.link' ).text link

    focus: ->
      @$( 'input[type=text]:first' ).focus()

    clear: ->
      @$( 'input[type=text]:first' ).val ''
