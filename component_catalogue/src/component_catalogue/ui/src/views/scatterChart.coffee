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
      console.log 'okay changed'
      return if not @chart
      do @chart.series[ 0 ]?.remove
      @chart.counters.color  = 0
      @chart.counters.symbol = 0
      @chart.addSeries series, redraw: true, animation: false
      console.log 'series added'

    render: ->
      @$el.html @chartContainer
      this

    tooltip: ( point )->
      options  = point.point.options
      date     = options.date
      index    = options.index
      roundedY = Math.round( point.y*100 )/100
      label    = @options.label
      unit     = @options.unit
      "Test ##{+index+1} of current series
       <br>Date: #{@formatDate date}
       <br>#{label}: #{roundedY} #{unit}"

    formatDate: ( date )->
      year    = date.getFullYear()
      month   = date.getMonth()
      minute  = date.getMinutes()
      hour    = date.getHours()
      day     = date.getDate()
      "#{day}.#{month}.#{year} #{hour}:#{minute}"

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
