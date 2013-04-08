define [ 'backbone', 'highcharts' ], ( Backbone, Highcharts )->
  Backbone.View.extend
    tagName: 'div'
    className: 'developer-chart'

    initialize: ->
      @model.listenTo @model, 'addSeries', @addSeries.bind @
      @model.listenTo @model, 'removeSeries', @removeSeries.bind @
      @chart = null

    addSeries: ( series )->
      @chart?.addSeries series, redraw: true, animation: 1000

    removeSeries: ( series )->
      do @chart.get( series.id ).remove

    render: ->
      chartContainer = $( '<div class="chart" />' ).appendTo( this.$el )
        
      chartContainer.highcharts do @model.highchartsConfig
      @chart = do chartContainer.highcharts
      this
