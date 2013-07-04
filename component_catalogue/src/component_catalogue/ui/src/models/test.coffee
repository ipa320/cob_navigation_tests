define [ 'backbone' ], ( Backbone )->
  Test = Backbone.Model.extend
    defaults:
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

    initialize: ->
      date = @get( 'localtime' )*1000
      @set 'date', new Date date
