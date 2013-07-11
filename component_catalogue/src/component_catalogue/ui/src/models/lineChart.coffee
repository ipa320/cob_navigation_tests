define [ 'backbone', 'models/noErroneousFilter'  ], ( Backbone, NoErroneousFilter )->

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

      if !sortingOptions.get 'showErrors'
        testGroup = testGroup.filter new NoErroneousFilter

      if 'date' != ( key = sortingOptions.get 'sorting' )
        testGroup = testGroup.sortBy key

      nameChunks = []
      for key in [ 'robot', 'navigation', 'scenario' ]
        nameChunks.push testGroup.get key


      data = testGroup?.getDetailedDataPointsForKey( @get 'key' )
      this.formatErrorPoints data
      name:  nameChunks.join ' / '
      id:    testGroup.id
      data:  data

    formatErrorPoints: ( data )->
      for i, current of data
        continue if !current.error

        previousY = +data[ i - 1 ]?.y || 0
        next      = @findNextValue data, i
        if next
          current.y = ( next.y - previousY ) / ( next.index - i + 1 ) + previousY
        else
          current.y = previousY

        current.marker = { symbol: 'square', fillColor: 'red' }

    findNextValue: ( data, i )->
      while current = data[ ++i ]
        if !current.error && +current.y
          return index: i, y: +current.y

    extremesChanged: ( min, max )->
      @_swallowNextExtremesEvent = true
      @get( 'filter' )?.setExtremes min, max

    setExtremes: ( range )->
      return @_swallowNextExtremesEvent = false if @_swallowNextExtremesEvent
      @set 'range', @get( 'filter' ).get 'range'

