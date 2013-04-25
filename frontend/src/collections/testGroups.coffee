define [ 'backbone', 'models/testGroup' ], ( Backbone, TestGroup )->
  Backbone.Collection.extend
    model: TestGroup

    constructor: ( models, options )->
      Backbone.Collection.apply this, arguments
      for model in @models
        model.set 'textFilter',   options.textFilter
        model.set 'dateFilter',   options.dateFilter
        model.set 'numberFilter', options.numberFilter
      this
