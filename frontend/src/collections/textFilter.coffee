define [ 'backbone', 'models/textFilterCriteria' ], ( Backbone, TextFilterCriteria )->
  Backbone.Collection.extend
    model: TextFilterCriteria
