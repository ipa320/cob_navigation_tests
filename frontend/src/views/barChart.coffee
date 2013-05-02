define [ 'backbone', 'highcharts-more', 'templates/tooltip' ], ( Backbone, Highcharts, tooltipTmpl )->
  Backbone.View.extend
    classname: '.application-view'
    tagName: 'div'
    elements: []


    initialize: ->
      @listenTo @model, 'change:hcSeries', @updateChart

    render: ( width )->
      chartContainer = $( '<div class="chart" />' ).appendTo( this.$el )
      chartContainer.width width if width
        
      chartContainer.highcharts do @highchartsConfig, ( chart ) => @chart = chart
      this

      
    updateChart: ->
      return if not @chart
      do @clear
      for series in @model.get 'hcSeries'
        copy = _.extend {}, series
        @chart.addSeries copy, true, null
      #do @redrawElements

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
        animation: false
        type: 'columnrange'
      plotOptions:
        series:
          animation: false
      series: []
      tooltip:
        shared: true
        formatter: @tooltipFormatter
      xAxis:
        categories: [ 'Duration', 'Distance', 'Rotation' ]

    redrawElements: ->
      console.log @chart
      for element in @elements
        element.destroy()
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


