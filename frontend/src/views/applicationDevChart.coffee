define [ 'backbone', 'templates/applicationDevChart', 'models/barChart', 'views/barChart' ], ( Backbone, applicationDevChartTmpl, BarChartModel, BarChartView )->
  Backbone.View.extend
    tagName:   'div'
    className: 'applicationDevChart'

    initialize: ->
      @listenTo @options.testGroups, 'change:empty change:selected', \
        _.debounce @groupsChanged.bind @, 10
      @chartModel = new BarChartModel
      @chartView  = new BarChartView model: @chartModel


    render: ->
      @$el.html do applicationDevChartTmpl
      @$( '.chart' ).html @chartView.render().el
      @


    groupsChanged: ->
      if do @validateTestGroups
        #@chart.set 'testGroups', testGroups
        do @showChart

    validateTestGroups: ->
      error = ''
      if not do @hasAtLeastOneSelectedRow
        error = 'No TestGroup selected'

      if not do @hasOnlyOneKindOfEveryFixedAttribute
        error  = "Testgroups selected are too diverse"

      @error error if error
      return !error.length

    hasAtLeastOneSelectedRow: ->
      @options.testGroups.any ( testGroup )=>
        return !testGroup.get( 'empty' ) and testGroup.get( 'selected' )

    hasOnlyOneKindOfEveryFixedAttribute: ->
      state = null
      @options.testGroups.every ( testGroup )=>
        return true if testGroup.get( 'empty' ) or !testGroup.get( 'selected' )
        id = ''
        id += testGroup.get key for key in @options.fixedAttributeKeys
        state = id if state == null
        return state == id

    hasNoVariableAttribute: ->
      return @testGroupAttributes[ @options.variableAttributeKey ].length == 0

    error: ( msg )->
      @$( '.error' ).show().html msg
      do @$( '.chart' ).hide

    showChart: ->
      do @$( '.chart' ).show
      do @$( '.error' ).hide
