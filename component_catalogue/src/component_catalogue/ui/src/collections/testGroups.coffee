define [ 'backbone', 'models/testGroup' ], ( Backbone, TestGroup )->
  Backbone.Collection.extend
    model: TestGroup

    constructor: ( models, options )->
      Backbone.Collection.apply @, arguments
      this
