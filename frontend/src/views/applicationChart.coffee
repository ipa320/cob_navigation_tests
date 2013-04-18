define [ 'backbone', 'highcharts-more' ], ( Backbone, Highcharts )->
  Backbone.View.extend
    classname: '.application-view'
    tagName: 'div'
    elements: []

    initialize: ->
      @model.listenTo @model, 'addSeries', @addSeries.bind @
      @model.listenTo @model, 'removeSeries', @removeSeries.bind @
      #@model.listenTo @model, 'change:range', @updateRange.bind @
      @chart = null

    render: ( width )->
      chartContainer = $( '<div class="chart" />' ).appendTo( this.$el )
      chartContainer.width width if width
        
      chartContainer.highcharts do @highchartsConfig, ( chart ) => @chart = chart
      this

    addSeries: ( series )->
      @chart.addSeries series, true, false
      do @redrawElements

    removeSeries: ( series )->
      do @chart.get( series.id ).remove
      do @redrawElements

    highchartsConfig: ->
      chart:
        animation: false
        type: 'columnrange'
      plotOptions: {}
      series: []
      xAxis:
        categories: [ 'Duration', 'Distance', 'Rotation' ]

    redrawElements: ->
      for element in @elements
        element.destroy()
      for series in @chart.series
        points = series.points
        plotLeft = @chart.plotLeft
        plotTop  = @chart.plotTop

        for point in points
          console.log( point )
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


