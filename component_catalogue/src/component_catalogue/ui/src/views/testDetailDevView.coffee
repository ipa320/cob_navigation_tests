define [ 'backbone', 'templates/testDetailDev', 'views/testDetailDevChart' ], ( Backbone, testDetailDevTmpl, TestDetailDevChart )->
  Backbone.View.extend
    tagName:   'div'
    className: 'testDetailDevView'
    events:
      'change:testGroup': 'testGroupChanged'

    initialize: ->
      @testGroup = null
      @deltaX = new TestDetailDevChart
        label: 'x', unit: 'm'
      @deltaY = new TestDetailDevChart
        label: 'y', unit: 'm'
      @deltaPhi = new TestDetailDevChart
        label: 'phi', unit: 'rad'

    useTestGroup: ( testGroup )->
      @stopListening @testGroup
      @testGroup = testGroup
      @listenTo @testGroup, 'change:selectedTest', @selectedTestChanged

    selectedTestChanged: ( testGroup, value )->
      tests = testGroup.get 'tests'
      test  = tests.at value
      if test
        deltas = test.get 'deltas'
        [ t, x, y, phi ] = @parseDeltas deltas
        @deltaX.renderDeltas t, x
        @deltaY.renderDeltas t, y
        @deltaPhi.renderDeltas t, phi

    parseDeltas: ( deltas )->
      t   = []
      x   = []
      y   = []
      phi = []
      for k,v of deltas
        t.push v[ 0 ]
        x.push v[ 1 ]
        y.push v[ 2 ]
        phi.push v[ 3 ]

      [ t, x, y, phi ]

    render: ->
      @$el.html do testDetailDevTmpl
      @$( '.deltaX' ).html @deltaX.render().el
      @$( '.deltaY' ).html @deltaY.render().el
      @$( '.deltaPhi' ).html @deltaPhi.render().el
      @

    renderNavigationChart: ->
      $el = @$ '.navigation'
      $el.html @navigationChart.render().el

    renderRobotChart: ->
      $el = @$ '.robot'
      $el.html @robotChart.render().el
