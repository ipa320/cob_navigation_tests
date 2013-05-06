define [ 'backbone', 'templates/applicationDevChart', 'models/barChart', 'views/barChart' ], ( Backbone, applicationDevChartTmpl, BarChartModel, BarChartView )->
  Backbone.View.extend
    tagName:   'div'
    className: 'applicationDevChart'

    initialize: ->
      @listenTo @options.testGroups, 'change:empty change:selected', \
        _.debounce @groupsChanged.bind @, 10
      @chartModel = new BarChartModel key: @options.variableAttributeKey
      @chartView  = new BarChartView model: @chartModel, title: @options.title


    render: ->
      @$el.html do applicationDevChartTmpl
      @$( '.chart' ).html @chartView.render().el
      do @groupsChanged
      @


    groupsChanged: ->
      testGroups = do @getInterestingRows
      if @validateTestGroups testGroups
        @chartModel.set 'testGroups', testGroups
        do @showChart

    validateTestGroups: ( rows )->
      error = ''
      if rows.length == 0
        error = 'No TestGroup selected'

      if not @hasOnlyOneKindOfEveryFixedAttribute rows
        error  = "Testgroups selected are too diverse"

      @error error if error
      return !error.length

    getInterestingRows: ->
      @options.testGroups.filter ( testGroup )->
        return true if !testGroup.get( 'empty' ) and testGroup.get( 'selected' )

    hasOnlyOneKindOfEveryFixedAttribute: ( rows )->
      state = null
      rows.every ( testGroup )=>
        for key in @options.fixedAttributeKeys
          id = ( id || '' ) + testGroup.get key
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
