define [ 'backbone', 'collections/testSeries' ], ( Backbone, TestSeries )->
  TestSeriesFiltered = Backbone.Model.extend
    defaults:
      robots:         []
      scenarios:      []
      algorithms:     []
      robot:          'None'
      scenario:       'None'
      algorithm:      'None'
      filteredSeries: null

    initialize: ( args, options )->
      @_collection = @collection || new Backbone.Collection
      do @reset
      do @updateAttributes

    reset: ->
      @collection = do @_collection.clone
      do @updateAttributes

    updateAttributes: ->
      for attr in [ 'robot', 'scenario', 'algorithm' ]
        @updateAttribute attr

    updateAttribute: ( attr )->
      values = _.uniq @getDataPointsForKey attr
      @attributes[ attr + 's' ] = values
      if values.length > 1
        @attributes[ attr ] = 'various'
      else if values.length == 1
        @attributes[ attr ] = values[ 0 ]
      else
        @attributes[ attr ] = 'None'

    filter: ( attributes )->
      @attributes.filteredSeries = @attributes.series.where attributes
      do @updateAttributes
      this

    getDataPointsForKey: ( key )->
      @attributes.filteredSeries.map ( testResult )->
        testResult.get key

    meanValue: ( key )->
      sum = 0
      dataPoints = @getDataPointsForKey key
      dataPoints.forEach ( value )->
        sum += value
      sum / dataPoints.length

    standardDeviation: ( key )->
      mean = @meanValue key
      dataPoints = @getDataPointsForKey key
      dataPoints.map ( value )->
        Math.sqrt Math.pow mean - value, 2

    toJSON: ->
      result = 
        id:        @id
        robot:     @attributes.robot
        scenario:  @attributes.scenario
        algorithm: @attributes.algorithm
        date:      @getDataPointsForKey 'date'
        length:    @attributes.filteredSeries.length
      for key in [ 'duration', 'rotation', 'distance' ]
        result[ 'mean.' + key ]   = @meanValue key
        result[ 'stdDev.' + key ] = @standardDeviation key
      result
