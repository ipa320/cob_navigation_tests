define [ 'backbone', 'highcharts' ], ( Backbone, Highcharts )->
  Backbone.View.extend
    tagName: 'div'
    className: 'developer-chart'

    initialize: ->
      @model.listenTo @model, 'addSeries', @addSeries.bind @
      @model.listenTo @model, 'removeSeries', @removeSeries.bind @
      @model.listenTo @model, 'change:range', @updateRange.bind @
      @chart = null

    addSeries: ( series )->
      console.log 'redraw'
      @chart?.addSeries series, redraw: true, animation: 1000

    removeSeries: ( series )->
      do @chart.get( series.id ).remove

    render: ( width )->
      chartContainer = $( '<div class="chart" />' ).appendTo( this.$el )
      chartContainer.width width if width
        
      chartContainer.highcharts do @highchartsConfig, ( chart ) =>
        @chart = chart
      this

    updateRange: ->
      range = @model.get 'range'
      @chart.xAxis[ 0 ].setExtremes range[ 0 ], range[ 1 ], true, false

    highchartsConfig: ->
      chart:
        type: 'line'
      series: []
      title:
        text: @model.get 'title'
      xAxis:
        events:
          setExtremes: ( e )=>@extremesChanged e.min, e.max
      credits:
        enabled: false
      scrollbar:
        enabled: false
      rangeSelector:
        enabled: false
