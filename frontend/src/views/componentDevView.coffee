define  [ 'backbone', 'views/devChart', 'templates/devCharts' ], ( Backbone, DevChart, devChartsTmpl )->
  Backbone.View.extend
    tagName:   'div'
    className: 'devCharts'

    initialize: ->

    render: ->
      @$el.html do devChartsTmpl
      @renderChart 'algorithm'
      @

    renderChart: ( key )->
      devChart = new DevChart
        key: key
        testGroups: @options.testGroups
      @$( ".#{key}" ).html devChart.render().el
