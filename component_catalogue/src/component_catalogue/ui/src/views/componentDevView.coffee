define  [ 'backbone', 'views/componentDevChart', 'templates/componentDev' ], ( Backbone, ComponentDevChart, componentDevTmpl, SortingOptions )->
  Backbone.View.extend
    tagName:   'div'
    className: 'componentDevView'

    initialize: ->
      @createChart 'duration', 'Duration', 's'
      @createChart 'distance', 'Distance', 'm'
      @createChart 'rotation', 'Rotation', 'deg'

    render: ->
      @$el.html do componentDevTmpl
      @renderChart 'duration'
      @renderChart 'distance'
      @renderChart 'rotation'
      @

    createChart: ( key, label, unit )->
      @charts = @charts ? []
      @charts[ key ] = new ComponentDevChart
        key:            key
        testGroups:     @options.testGroups
        sortingOptions: @options.sortingOptions
        label:          label
        unit:           unit

    renderChart: ( key )->
      @$( ".#{key}" ).html @charts[ key ].render().el

