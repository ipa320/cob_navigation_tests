define [ 'backbone', 'models/testResult' ], ( Backbone, TestResult )->
  Backbone.Collection.extend
    model: TestResult

