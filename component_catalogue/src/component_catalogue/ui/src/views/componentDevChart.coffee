define [ 'backbone', 'templates/componentDevChart', 'models/componentDevLineChart', 'views/lineChart' ], ( Backbone, chartTmpl, LineChart, LineChartView )->
  Backbone.View.extend
    tagName:   'div'
    className: 'componentDevChart'

    # most of the times, several resize triggers are issued with small or no
    # time difference. Group all those together
    triggerResize: _.debounce ->
      $( window ).trigger 'resize'
    , 20

    initialize: ->
      @listenTo @options.testGroups, 'change:empty change:selected',
        _.debounce @groupsChanged.bind( @ ), 20

      @lineChartModel = new LineChart
        key:            @options.key
        sortingOptions: @options.sortingOptions
      @lineChartView = new LineChartView
        model: @lineChartModel
        label: @options.label
        unit:  @options.unit

      @triggerResizeOnce = _.once @triggerResize

    render: ->
      @$el.html do chartTmpl
      @$( '.chart' ).html @lineChartView.render().el
      do @groupsChanged
      @

    groupsChanged: ->
      models = []
      @options.testGroups.each ( testGroup )=>
        if testGroup.get( 'selected' ) and !testGroup.get 'empty'
          models.push testGroup

      switch models.length
        when 0 then do @noItemSelected
        when 1 then @oneItemSelected models[ 0 ]
        else do @multipleItemsSelected

    noItemSelected: ->
      @errorOccured 'no item selected'

    multipleItemsSelected: ->
      @errorOccured 'multiple items selected'

    oneItemSelected: ( testGroup )->
      do @noError
      @lineChartModel.set 'testGroup',  testGroup

    errorOccured: ( msg )->
      @$( '.error' ).show().html msg
      @$( '.chart' ).hide()
      @lineChartModel.set 'testGroup', null

    noError: ->
      @$( '.error' ).hide()
      chart = @$ '.chart'
      if !chart.is ':visible'
        chart.show()
        do @triggerResizeOnce
