define [ 'backbone', 'templates/testDetailDev', 'views/testDetailDevChart' ], ( Backbone, testDetailDevTmpl, TestDetailDevChart )->
  Backbone.View.extend
    tagName:   'div'
    className: 'testDetailDevView'
    events:
      'change:testGroup': 'testGroupChanged'

    initialize: ->
      @testGroup = null
      @deltaX = new TestDetailDevChart
        label: 'x', unit: ''
      @deltaY = new TestDetailDevChart
        label: 'y', unit: ''
      @deltaZ = new TestDetailDevChart
        label: 'z', unit: ''

    useTestGroup: ( testGroup )->
      @stopListening @testGroup
      @testGroup = testGroup
      @listenTo @testGroup, 'change:selectedTest', @selectedTestChanged

    selectedTestChanged: ( testGroup, value )->
      tests = testGroup.get 'tests'
      test  = tests.at value
      if test
        deltas = test.get 'deltas'
        [ t, x, y, z ] = @parseDeltas deltas
        @deltaX.renderDeltas t, x
        @deltaY.renderDeltas t, y
        @deltaZ.renderDeltas t, z

    parseDeltas: ( deltas )->
      t = []
      x = []
      y = []
      z = []
      for k,v of deltas
        t.push v[ 0 ]
        x.push v[ 1 ]
        y.push v[ 2 ]
        z.push v[ 3 ]

      [ t, x, y, z ]

    render: ->
      @$el.html do testDetailDevTmpl
      @$( '.deltaX' ).html @deltaX.render().el
      @$( '.deltaY' ).html @deltaY.render().el
      @$( '.deltaZ' ).html @deltaZ.render().el
      @

    renderNavigationChart: ->
      $el = @$ '.navigation'
      $el.html @navigationChart.render().el

    renderRobotChart: ->
      $el = @$ '.robot'
      $el.html @robotChart.render().el
