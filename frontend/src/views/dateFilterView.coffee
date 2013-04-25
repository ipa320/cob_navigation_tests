define [ 'backbone', 'templates/dateFilter', 'jquery-ui' ], ( Backbone, dateFilterTmpl, jqueryUi )->
  Backbone.View.extend
    tagName:    'div'
    className:  'dateFilter'
    dateFormat: 'dd.mm.yy'
    events:
      'click .start.clear': 'clearStart'
      'click .end.clear':   'clearEnd'

    render: ->
      @$el.html dateFilterTmpl {}
      @$( 'input.start' ).datepicker
        onClose: @startChanged.bind @
        dateFormat:  @dateFormat
      @$( 'input.end' ).datepicker
        onClose: @endChanged.bind @
        dateFormat:  @dateFormat
      this

    startChanged: ( selectedDate )->
      @$( 'input.end' ).datepicker 'option', 'minDate', selectedDate
      @options.dateFilter.set 'start', @$( '.start' ).datepicker 'getDate'

    endChanged: ( selectedDate )->
      @$( 'input.start' ).datepicker 'option', 'maxDate', selectedDate
      @options.dateFilter.set 'end', @$( '.end' ).datepicker 'getDate'

    clearStart: ( e )->
      @clearInput e.currentTarget
      @$( 'input.end' ).datepicker 'option', 'minDate', ''

    clearEnd: ( e ) ->
      @clearInput e.currentTarget
      @$( 'input.start' ).datepicker 'option', 'maxDate', ''

    clearInput: ( input )->
      input = $( input ).siblings( 'input' )
      input.val( '' )
      @options.dateFilter.set input.attr( 'name' ), null
