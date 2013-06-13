define [ 'backbone', 'templates/numberFilter', 'jquery-numeric' ], ( Backbone, numberFilterTmpl, numeric )->
  Backbone.View.extend
    tagName:   'div'
    className: 'numberFilter'
    events:
      'keyup .count': 'change'

    render: ->
      @$el.html numberFilterTmpl {}
      @$( '.count' ).numeric
        decimal:  false
        negative: false
      this

    initialize: ->
      @deferedUpdate = _.debounce ( value )=>
        @options.numberFilter.set 'count', value
      , 200

    change: ( e )->
      input = @$ '.count'
      if e.keyCode == 27
        input.val ''
      @deferedUpdate input.val()
