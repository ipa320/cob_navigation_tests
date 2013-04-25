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

    change: ->
      input = @$ '.count'
      @options.numberFilter.set 'count', input.val()

