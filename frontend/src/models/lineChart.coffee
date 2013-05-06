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
      @listenTo @get( 'sortingOptions' ), 'change', @sortingChanged
      
    testGroupChanged: ->
      testGroup = @get 'testGroup'
      @stopListening @previous 'testGroup' if @previous 'testGroup'
      @listenTo testGroup, 'change', @updateHcSeries if testGroup
      do @updateHcSeries

    sortingChanged: ->
      do @updateHcSeries

    updateHcSeries: ->
      @set 'hcSeries', do @asHighchartsSeries

    asHighchartsSeries: ->
      testGroup      = @get 'testGroup'
      sortingOptions = @get 'sortingOptions'
      return {} if not testGroup

      if 'value' == sortingOptions.get 'sorting'
        key = @get 'key'
        testGroup = testGroup.sortBy ( model )-> model.get key

      nameChunks = []
      for key in [ 'robot', 'algorithm', 'scenario' ]
        nameChunks.push testGroup.get key


      date = testGroup?.getDataPointsForKey( 'date' )
      data = testGroup?.getDetailedDataPointsForKey( @get 'key' )
      name:  nameChunks.join ' / '
      id:    testGroup.id
      data:  data

    extremesChanged: ( min, max )->
      @_swallowNextExtremesEvent = true
      @get( 'filter' )?.setExtremes min, max

    setExtremes: ( range )->
      return @_swallowNextExtremesEvent = false if @_swallowNextExtremesEvent
      @set 'range', @get( 'filter' ).get 'range'

