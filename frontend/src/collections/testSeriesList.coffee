define [ 'backbone', 'models/testSeries' ], ( Backbone, TestSeries )->
  Backbone.Collection.extend
    model: TestSeries

    toAnalyzedJSON: ()->
      @models.map ( model )->
        do model.toAnalyzedJSON
