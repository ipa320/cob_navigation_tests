define  [ 'backbone', 'views/componentDevChart', 'templates/componentDev', 'models/sortingOptions', 'views/sortingOptions' ], ( Backbone, ComponentDevChart, componentDevTmpl, SortingOptions, SortingOptionsView )->
  Backbone.View.extend
    tagName:   'div'
    className: 'componentDevView'

    initialize: ->
      @sortingOptions = new SortingOptions
      
      @createChart 'duration', 'Duration', 's'
      @createChart 'distance', 'Distance', 'm'
      @createChart 'rotation', 'Rotation', 'deg'

    render: ->
      @$el.html do componentDevTmpl
      @renderChart 'duration'
      @renderChart 'distance'
      @renderChart 'rotation'
      do @renderSortingOptions
      @

    createChart: ( key, label, unit )->
      @charts = @charts ? []
      @charts[ key ] = new ComponentDevChart
        key:            key
        testGroups:     @options.testGroups
        sortingOptions: @sortingOptions
        label:          label
        unit:           unit

    renderChart: ( key )->
      @$( ".#{key}" ).html @charts[ key ].render().el

    renderSortingOptions: ->
      sortingOptions = new SortingOptionsView
        model: @sortingOptions
      @$( '.sortingOptionsContainer' ).html sortingOptions.render().el
