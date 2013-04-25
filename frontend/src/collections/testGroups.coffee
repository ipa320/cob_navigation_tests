define [ 'backbone', 'models/testGroup' ], ( Backbone, TestGroup )->
  Backbone.Collection.extend
    model: TestGroup

    constructor: ( models, options )->
      Backbone.Collection.apply @, arguments

      for model in @models
        model.set 'filters', options.filters
      this
