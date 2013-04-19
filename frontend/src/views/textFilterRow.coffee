define [ 'backbone', 'templates/textFilterRow', 'chosen' ], ( Backbone, textFilterRowTmpl, chosen )->
  Backbone.View.extend
    tagName: 'div'
    className: 'textFilterRow'
    events:
      'change':     'change'
      'keyup':      'keyup'
      'click .and': 'setAndLink'
      'click .or':  'setOrLink'

    render: ->
      @$el.html textFilterRowTmpl()
      this

    keyup: ( e )->
      if e.keyCode == 27
        @trigger 'escape'
      do @change

    change: ->
      @options.criteria.set 'field', @$( '.filterField' ).val()
      @options.criteria.set 'type',  @$( '.filterType'  ).val()
      @options.criteria.set 'value', $.trim( @$( '.filterValue' ).val())

    setAndLink: ->
      @$( '.and, .or' ).hide()
      @$( '.link' ).text( 'and' )
      @options.criteria.set 'link', 'and'

    setOrLink: ->
      @$( '.and, .or' ).hide()
      @$( '.link' ).text( 'or' )
      @options.criteria.set 'link', 'or'

    focus: ->
      @$( 'input[type=text]:first' ).focus()

