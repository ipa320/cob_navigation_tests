define [ 'backbone', 'models/testDetailScatterChart', 'views/scatterChart' ], ( Backbone, ScatterChart, ScatterChartView )->
  Backbone.View.extend
    tagName:   'div'
    className: 'testDetailDevChart'

    initialize: ->
      @chartModel = new ScatterChart

      @chartView = new ScatterChartView
        model: @chartModel
        label: @options.label
        unit:  @options.unit

    renderDeltas: ( t, deltas )->
      @chartModel.updateDeltas t, deltas

    render: ->
      @$el.html @chartView.render().el
      @

    renderDataset: ->
