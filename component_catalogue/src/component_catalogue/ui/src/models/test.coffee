define [ 'backbone' ], ( Backbone )->
  Test = Backbone.Model.extend
    defaults:
      active:      true
      deltas:      []
      error:       ''
      collisions:  0
      date:        0
      robot:       ''
      scenario:    ''
      navigation:  ''
      testResults: null
      duration:    null
      distance:    null
      rotation:    null
      video:       'lol'

    initialize: ->
      date = @get( 'localtime' )*1000
      @set 'date', new Date date

    applyFilters: ( filters )->
      for filter in filters
        if !filter.complies @
          return @set 'active', false
      @set 'active', true
