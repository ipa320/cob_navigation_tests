define [ 'backbone' ], ( Backbone )->
  Test = Backbone.Model.extend
    defaults:
      date: 0
      robot: ''
      scenario: ''
      algorithm: ''
      tooSexy: 'yes'
      testResults: null
      duration:  null
      distance:  null
      rotation:  null

    initialize: ->
      date = @get 'date'
      if !( date instanceof Date )
        @set 'date', new Date date