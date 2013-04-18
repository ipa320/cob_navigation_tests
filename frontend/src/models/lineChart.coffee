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
      @get( 'groups' )?.bind 'change:selected', @selectChange, this
      @get( 'filter' )?.bind 'change:range', @setExtremes, this
      
    selectChange: ( model, selected )->
      hcSeries = @testGroupToHighchartSeries model
      events = [ 'removeSeries', 'addSeries' ]
      @trigger events[ +selected ], hcSeries

    testGroupToHighchartSeries: ( model )->
      nameChunks = []
      for key in [ 'robot', 'algorithm', 'scenario' ]
        nameChunks.push model.get key

      date = model.getDataPointsForKey( 'date' )
      data = model.getDataPointsForKey( @attributes.key )
      name:  nameChunks.join ' / '
      id:    model.id
      data:  _.zip date, data


    extremesChanged: ( min, max )->
      @_swallowNextExtremesEvent = true
      @get( 'filter' )?.setExtremes min, max

    setExtremes: ( range )->
      return @_swallowNextExtremesEvent = false if @_swallowNextExtremesEvent
      @set 'range', @get( 'filter' ).get 'range'

