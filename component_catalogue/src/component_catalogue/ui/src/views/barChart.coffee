define [ 'backbone', 'highcharts-more', 'templates/tooltip' ], ( Backbone, Highcharts, tooltipTmpl )->
  Backbone.View.extend
    classname: '.application-view'
    tagName: 'div'

    initialize: ->
      @listenTo @model, 'change:hcSeries', _.debounce @updateChart.bind( @ ), 20
      @id = _.uniqueId 'appChart'
      @elements = []

      @chartContainer = chartContainer = $( '<div class="chart" />' )
      @chartContainer.highcharts do @highchartsConfig, ( chart ) =>
        @chart = chart

    render: ( width )->
      @$el.html @chartContainer
      this

      
    updateChart: ->
      return if not @chart
      do @clear
      for series in @model.get 'hcSeries'
        copy = _.extend {}, series
        @chart.addSeries copy, false, null
      do @chart.redraw

    clear: ->
      @chart.counters.color = 0
      while @chart.series.length
        @chart.series[ 0 ].remove false

    tooltipFormatter: ->
      units =
        duration: 'min'
        distance: 'm'
        rotation: 'deg'
      values = @points.map ( point )->
        mean   = ( point.point.high+point.point.low ) / 2
        stdDev = point.point.high - mean
        label:  point.series.name
        mean:   Math.round( mean*100 ) / 100
        stdDev: Math.round( stdDev*100 ) / 100
        color:  point.series.color

      tooltipTmpl
        name:   @x
        points: values
        unit:   units[ @x.toLowerCase() ] || ''

    highchartsConfig: ->
      chart:
        animation:   false
        type:        'columnrange'
        events:
          redraw:    @redrawElements.bind @
      title:
        text:        @options.title
      plotOptions:
        series:
          animation: false
      yAxis: [
        title:
          text:      ''
        ,
        title:
          text: ''
        ,
        title:
          text: ''
      ]
      series:        []
      tooltip:
        shared:      true
        formatter:   @tooltipFormatter
      xAxis:
        categories:  [ 'Duration', 'Distance', 'Rotation' ]

    redrawElements: ->
      if @elements.length
        for element in @elements
          element.destroy()
        @elements = []

      for series in @chart.series
        points = series.points
        plotLeft = @chart.plotLeft
        plotTop  = @chart.plotTop

        for point in points
          shape = point.shapeArgs
          rect = @chart.renderer.rect(
            shape.x + plotLeft,
            shape.y + plotTop + shape.height/2,
            shape.width, 2 )

          rect.attr({
            'stroke-width': 0,
            'fill': 'white'
          }).add().toFront()
          @elements.push rect
