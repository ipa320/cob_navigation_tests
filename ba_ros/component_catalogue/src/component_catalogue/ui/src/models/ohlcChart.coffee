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
      @get( 'groups' )?.bind 'select', @groupSelected, this
      @get( 'groups' )?.bind 'unselect', @groupUnselected, this
      @get( 'filter' )?.bind 'change:range', @setExtremes, this
      
    groupSelected: ( model )->
      hcSeries = @testGroupToHighchartSeries model
      @trigger 'addSeries', hcSeries

    groupUnselected: ( model )->
      hcSeries = @testGroupToHighchartSeries model
      this.trigger 'removeSeries', hcSeries

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

    highchartsConfig: ->
      series: []
      title:
        text: @attributes.title
      xAxis:
        events:
          setExtremes: ( e )=>@extremesChanged e.min, e.max
      credits:
        enabled: false
      scrollbar:
        enabled: false
      rangeSelector:
        enabled: false
