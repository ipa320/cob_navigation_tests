define [ 'backbone', 'templates/dateFilter', 'jquery-ui' ], ( Backbone, dateFilterTmpl, jqueryUi )->
  Backbone.View.extend
    tagName:    'div'
    className:  'dateFilter'
    dateFormat: 'dd.mm.yy'
    events:
      'click .clear': 'clear'

    render: ->
      @$el.html dateFilterTmpl {}
      @$( '.start' ).datepicker
        onClose: @startChanged.bind @
        dateFormat:  @dateFormat
      @$( '.end' ).datepicker
        onClose: @endChanged.bind @
        dateFormat:  @dateFormat
      this

    startChanged: ( selectedDate )->
      @$( '.end' ).datepicker 'option', 'minDate', selectedDate
      @options.dateFilter.set 'start', @$( '.start' ).datepicker 'getDate'

    endChanged: ( selectedDate )->
      @$( '.start' ).datepicker 'option', 'maxDate', selectedDate
      @options.dateFilter.set 'end', @$( '.end' ).datepicker 'getDate'

    clear: ( e )->
      input = $( e.currentTarget ).siblings( 'input' )
      input.val( '' )
      @options.dateFilter.set input.attr( 'name' ), null
