define [ 'backbone' ], ( Backbone )->
  Backbone.Model.extend
    defaults:
      count: -1

    complies: ( test )->
      count = @get 'count'
      return true if count < 0

      minDate = do @getMinDate
      return test.get( 'date' ) >= minDate

    getMinDate: ->
      tests = @get 'tests'
      count = @get 'count'
      tests.at( tests.length - count ).get 'date'
