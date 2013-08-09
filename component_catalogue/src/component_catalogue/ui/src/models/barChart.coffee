define [ 'backbone'  ], ( Backbone )->

  Backbone.Model.extend
    defaults:
      testGroups:       null
      key:             ''
      title:           ''
      xAxisCategories: null
      yAxisLabel:      ''
      valueSuffix:     ''
      filter:          null

    initialize: ->
      @on  'change:testGroups', @testGroupsChanged
      
    testGroupsChanged: ->
      do @stopListeningToPreviousTestGroups
      for testGroup in @get 'testGroups'
        @listenTo testGroup, 'change', _.debounce @updateHcSeries, 200
      do @updateHcSeries

    stopListeningToPreviousTestGroups: ->
      prevTestGroups = @previous 'testGroups'
      return if not prevTestGroups
      for testGroup in prevTestGroups
        @stopListening testGroup

    updateHcSeries: ->
      oldHcSeries = @get 'hcSeries'
      newHcSeries = do @asHighchartsSeries
      if !_.isEqual oldHcSeries, newHcSeries
        @set 'hcSeries', newHcSeries

    asHighchartsSeries: ()->
      series = []
      key    = @get 'key'
      for testGroup in @get 'testGroups'
        data = []
        mean   = ( +testGroup.get 'mean.'   + key ) || 0
        stdDev = ( +testGroup.get 'stdDev.' + key ) || 0
        data.push [ mean - stdDev, mean + stdDev ]

        series.push
          name:  testGroup.get @get 'variableKey'
          id:    testGroup.id
          data:  data
          
      _.sortBy series, ( item )-> item.name
