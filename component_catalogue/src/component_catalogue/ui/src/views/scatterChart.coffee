define [ 'backbone', 'highcharts' ], ( Backbone, Highcharts )->
  Backbone.View.extend
    tagName:   'div'
    className: 'scatterChart'

    initialize: ->
      @listenTo @model, 'change:hcSeries', _.debounce @resetSeries.bind( @ ), 20
      @chart = null

      @chartContainer = chartContainer = $( '<div class="chart" />' )
      chartContainer.highcharts do @highchartsConfig, ( chart ) =>
        @chart = chart

    resetSeries: ( model, series )->
      return if not @chart
      do @chart.series[ 0 ]?.remove
      @chart.counters.color  = 0
      @chart.counters.symbol = 0
      @chart.addSeries series, redraw: true, animation: false

    render: ->
      @$el.html @chartContainer
      this

    tooltip: ( point )->
      "Timestamp: #{point.x}<br>
      Value: #{point.y}"

    highchartsConfig: ->
      self = @
      chart:
        type: 'scatter'
        animation: false
      title:
        text:        "#{@options.label} in #{@options.unit}"
      tooltip:
        formatter: -> self.tooltip this
      plotOptions:
        series:
          animation: false
      yAxis:
        title:
          text: null
      series: []
      legend:
        enabled: false
      credits:
        enabled: false
      scrollbar:
        enabled: false
      rangeSelector:
        enabled: false
