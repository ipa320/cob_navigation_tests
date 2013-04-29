define [ 'backbone'  ], ( Backbone )->

  Backbone.Model.extend
    defaults:
      testGroup:       undefined
      hcSeries:        undefined
      key:             ''
      title:           ''
      xAxisCategories: null
      yAxisLabel:      ''
      valueSuffix:     ''
      filter:          null

    initialize: ->
      @on 'change:testGroup', @testGroupChanged
      
    testGroupChanged: ->
      testGroup = @get 'testGroup'
      @stopListening @previous 'testGroup'
      @listenTo testGroup, 'change', @updateHcSeries if testGroup
      do @updateHcSeries

    updateHcSeries: ->
      @set 'hcSeries', do @asHighchartsSeries

    asHighchartsSeries: ->
      testGroup  = @get 'testGroup'
      return {} if not testGroup

      nameChunks = []
      for key in [ 'robot', 'algorithm', 'scenario' ]
        nameChunks.push testGroup.get key

      date = testGroup?.getDataPointsForKey( 'date' )
      data = testGroup.getDataPointsForKey( @get 'key' )
      name:  nameChunks.join ' / '
      id:    testGroup.id
      data:  _.zip date, data

    extremesChanged: ( min, max )->
      @_swallowNextExtremesEvent = true
      @get( 'filter' )?.setExtremes min, max

    setExtremes: ( range )->
      return @_swallowNextExtremesEvent = false if @_swallowNextExtremesEvent
      @set 'range', @get( 'filter' ).get 'range'

