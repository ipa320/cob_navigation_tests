define [ 'backbone' ], ( Backbone )->
  Backbone.Model.extend
    defaults:
      count: -1
<<<<<<< HEAD

    complies: ( number, test )->
      count = @get 'count'
      return !number || !( count > 0 ) || number < count
