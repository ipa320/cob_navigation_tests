define [ 'backbone', 'templates/componentDevChart', 'models/lineChart', 'views/lineChart' ], ( Backbone, chartTmpl, LineChart, LineChartView )->
  Backbone.View.extend
    tagName:   'div'
    className: 'componentDevChart'

    initialize: ->
      @listenTo @options.testGroups, 'change:empty change:selected',
        @groupsChanged

      @lineChartModel = new LineChart
        key:            @options.key
        sortingOptions: @options.sortingOptions
      @lineChartView = new LineChartView
        model: @lineChartModel
        label: @options.label
        unit:  @options.unit

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
        $( window ).trigger 'resize'
