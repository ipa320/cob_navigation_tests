define [ 'backbone'  ], ( Backbone )->

  Backbone.Model.extend
    defaults:
      key: ''
      title: ''
      xAxisCategories: null
      yAxisLabel: ''
      valueSuffix: ''
      filter: null

    initialize: ->
      @get( 'groups' )?.bind 'change:selected', @selectChanged, this
      @get( 'filter' )?.bind 'change:range', @setExtremes, this
      
    selectChanged: ( model, selected )->
      hcSeries = @testGroupToHighchartSeries model
      events = [ 'removeSeries', 'addSeries' ]
      @trigger events[ +selected ], hcSeries

    testGroupToHighchartSeries: ( model )->
      nameChunks = []
      for key in [ 'robot', 'algorithm', 'scenario' ]
        nameChunks.push model.get key

      mean   = model.get 'mean.'   + @get 'key'
      stdDev = model.get 'stdDev.' + @get 'key'
      console.log mean, stdDev

      name:  nameChunks.join ' / '
      id:    model.id
      data:  [[ mean - stdDev, mean + stdDev ], [ 0,2 ]]

    extremesChanged: ( min, max )->
      @_swallowNextExtremesEvent = true
      @get( 'filter' )?.setExtremes min, max

    setExtremes: ( range )->
      return @_swallowNextExtremesEvent = false if @_swallowNextExtremesEvent
      @set 'range', @get( 'filter' ).get 'range'
