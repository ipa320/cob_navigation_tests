define [ 'backbone', 'models/testGroup' ], ( Backbone, TestGroup )->
  Backbone.Collection.extend
    model: TestGroup

    constructor: ( models, options )->
      Backbone.Collection.apply this, arguments
      @on 'changed', -> console.log 'changed'
      for model in @models
        model.set 'textFilter', options.textFilter
      #options.filter?.on 'change', @filterChanged
      this
