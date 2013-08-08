define [ 'backbone' ], ( Backbone )->
  Backbone.Model.extend
    defaults:
      show: true

    complies: ( test )->
      return true if @get 'show'
      return !test.get 'error'


