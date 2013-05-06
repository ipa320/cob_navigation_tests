define  [ 'backbone', 'views/componentDevChart', 'templates/componentDev', 'models/sortingOptions', 'views/sortingOptions' ], ( Backbone, ComponentDevChart, componentDevTmpl, SortingOptions, SortingOptionsView )->
  Backbone.View.extend
    tagName:   'div'
    className: 'componentDevView'

    initialize: ->
      @sortingOptions = new SortingOptions

    render: ->
      @$el.html do componentDevTmpl
      @renderChart 'duration', 'Duration', 's'
      @renderChart 'distance', 'Distance', 'm'
      @renderChart 'rotation', 'Rotation', 'deg'
      do @renderSortingOptions
      @

    renderChart: ( key, label, unit )->
      chart = new ComponentDevChart
        key:            key
        testGroups:     @options.testGroups
        sortingOptions: @sortingOptions
        label:          label
        unit:           unit
      @$( ".#{key}" ).html chart.render().el

    renderSortingOptions: ->
      sortingOptions = new SortingOptionsView
        model: @sortingOptions
      @$( '.sortingOptionsContainer' ).html sortingOptions.render().el
