define [ 'backbone', 'models/testGroup' ], ( Backbone, TestGroup )->
  Backbone.Collection.extend
    model: TestGroup
