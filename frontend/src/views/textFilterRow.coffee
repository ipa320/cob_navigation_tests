define [ 'backbone', 'templates/textFilterRow', 'chosen' ], ( Backbone, textFilterRowTmpl, chosen )->
  Backbone.View.extend
    tagName: 'div'
    className: 'textFilterRow'
    events:
      'change':     'change'
      'keyup':      'keyup'
      'click .and': 'setAndLink'
      'click .or':  'setOrLink'

    initialize: ->
      @listenTo @model, 'change:link', @linkChanged

    render: ->
      @$el.html textFilterRowTmpl()
      this

    keyup: ( e )->
      if e.keyCode == 27
        @trigger 'escape'
      do @change

    change: ->
      @model.set 'field', @$( '.filterField' ).val()
      @model.set 'type',  @$( '.filterType'  ).val()
      @model.set 'value', $.trim( @$( '.filterValue' ).val())

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

