define [ 'backbone', 'templates/applicationDevChart', 'models/barChart', 'views/barChart' ], ( Backbone, applicationDevChartTmpl, BarChartModel, BarChartView )->
  Backbone.View.extend
    tagName:   'div'
    className: 'applicationDevChart'

    initialize: ->
      @listenTo @options.testGroups, 'change:count change:selected', \
        _.debounce @groupsChanged.bind @, 10
      @triggerResizeOnce = _.once @triggerResize

      @chartModels = []
      @chartViews  = []
      for key in [ 'duration', 'distance', 'rotation' ]
        model = new BarChartModel
          key: key
          variableKey: @options.variableAttributeKey # think of a better name
        @chartModels.push model
        @chartViews.push new BarChartView
          model: model
          title: @options.title
          key:   key

    # most of the times, several resize triggers are issued with small or no
    # time difference. Group all those together
    triggerResize: _.debounce ->
      $( window ).trigger 'resize'
    , 20

    render: ->
      @$el.html do applicationDevChartTmpl
      for i, view of @chartViews
        @$( ".chart_#{i}" ).html view.render().el
      do @groupsChanged
      @


    groupsChanged: ->
      testGroups = do @getInterestingRows
      if @validateTestGroups testGroups
        for key, model of @chartModels
          model.set 'testGroups', testGroups
        do @showCharts

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
        return true if testGroup.get( 'count' ) > 0 and testGroup.get( 'selected' )

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
      @$el.parent().hide()
      #@$( '.error' ).show().html msg
      #@$( '.error' ).hide()
      do @$( '.charts' ).hide

    showCharts: ->
      @$el.parent().show()
      do @$( '.charts' ).show
      do @$( '.error' ).hide
      do @triggerResizeOnce
