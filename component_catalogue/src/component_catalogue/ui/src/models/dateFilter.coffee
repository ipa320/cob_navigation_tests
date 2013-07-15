define [ 'backbone' ], ( Backbone )->
  Backbone.Model.extend
    defaults:
      start: ''
      end:   ''

    complies: ( test )->
      date  = test.get 'date'
      start = @get 'start'
      end   = @get 'end'
      ( !start || date >= start ) && ( !end || date <= end )
