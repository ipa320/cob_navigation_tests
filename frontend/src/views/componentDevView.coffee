define  [ 'backbone', 'views/componentDevChart', 'templates/componentDev' ], ( Backbone, ComponentDevChart, componentDevTmpl )->
  Backbone.View.extend
    tagName:   'div'
    className: 'componentDev'

    initialize: ->

    render: ->
      @$el.html do componentDevTmpl
      @renderChart 'duration'
      @renderChart 'distance'
      @renderChart 'rotation'
      @

    renderChart: ( key )->
      chart = new ComponentDevChart
        key: key
        testGroups: @options.testGroups
      @$( ".#{key}" ).html chart.render().el
