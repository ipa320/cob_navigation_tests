define [ 'backbone', 'collections/testResults' ], ( Backbone, TestResults )->
  Backbone.Model.extend
    defaults:
      date: 0
      robot: ''
      scenario: ''
      algorithm: ''
      tooSexy: 'yes'
      testResults: null

    initialize: ( args, options )->
      @attributes.testResults = new TestResults args?.testResults || []

    meanValue: ( key )->
      sum = 0
      @attributes.testResults.each ( testResult )->
        sum += testResult.get key
      sum / @attributes.testResults.length

    standardDeviation: ( key )->
      mean = @meanValue key
      @attributes.testResults.map ( testResult )->
        value = testResult.get key
        Math.sqrt Math.pow mean - value, 2

    toAnalyzedJSON: ->
      keys = [ 'duration', 'rotation', 'distance' ]
      result = 
        robot:     @attributes.robot
        scenario:  @attributes.scenario
        algorithm: @attributes.algorithm
        date:      @attributes.date
      for key in keys
        result[ 'mean.' + key ]   = @meanValue key
        result[ 'stdDev.' + key ] = @standardDeviation key
      result
