define [ 'backbone' ], ( Backbone )->
  Backbone.Model.extend
    defaults:
      sorting: 'date'
      showErrors:  true
