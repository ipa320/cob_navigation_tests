define [ 'backbone', 'models/testDetailLineChart', 'views/lineChart' ], ( Backbone, LineChart, LineChartView )->
  Backbone.View.extend
    tagName:   'div'
    className: 'testDetailDevChart'

    initialize: ->
      @lineChartModel = new LineChart

      @lineChartView = new LineChartView
        model: @lineChartModel
        label: @options.label
        unit:  @options.unit

    renderDeltas: ( t, deltas )->
      @lineChartModel.updateDeltas t, deltas

    render: ->
      @$el.html @lineChartView.render().el
      @

    renderDataset: ->
