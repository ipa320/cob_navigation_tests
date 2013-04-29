define [ 'backbone', 'highcharts' ], ( Backbone, Highcharts )->
  Backbone.View.extend
    tagName:   'div'
    className: 'lineChart'

    initialize: ->
      @listenTo @model, 'change:hcSeries',  _.debounce @resetSeries, 500
      @chart = null

    resetSeries: ( model, series )->
      do @chart.series[ 0 ]?.remove
      @chart.addSeries series, redraw: true, animation: false

    render: ->
      chartContainer = $( '<div class="chart" />' ).appendTo( @$el )
      chartContainer.highcharts do @highchartsConfig, ( chart ) =>
        @chart = chart
      this

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
