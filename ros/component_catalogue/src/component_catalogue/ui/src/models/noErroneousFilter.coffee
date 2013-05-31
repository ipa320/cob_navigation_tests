define [ 'backbone' ], ( Backbone )->
  Backbone.Model.extend
    complies: ( number, test )->
      return !test.get 'error'
