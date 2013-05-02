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
      @
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
      for testGroup in @get 'testGroups'
        data = []
        for key in [ 'duration', 'distance', 'rotation' ]
          mean   = testGroup.get 'mean.'   + key
          stdDev = testGroup.get 'stdDev.' + key
          data.push [ mean - stdDev, mean + stdDev ]

        series.push
          name:  testGroup.get @get 'key'
          id:    testGroup.id
          data:  data

      series
