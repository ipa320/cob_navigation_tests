define [ 'backbone', 'templates/applicationDev', 'views/applicationDevChart' ], ( Backbone, applicationDevTmpl, ApplicationDevChart )->
  Backbone.View.extend
    tagName:   'div'
    className: 'applicationDevView'

    initialize: ->
      @algorithmChart = new ApplicationDevChart
        testGroups:           @options.testGroups
        variableAttributeKey: 'algorithm'
        fixedAttributeKeys:   [ 'robot', 'scenario' ]
        title: 'Different algorithms for fixed robot and scenario'

      @robotChart = new ApplicationDevChart
        testGroups:           @options.testGroups
        variableAttributeKey: 'robot'
        fixedAttributeKeys:   [ 'algorithm', 'scenario' ]
        title: 'Different robots for fixed algorithms and scenario'

    render: ->
      @$el.html do applicationDevTmpl
      do @renderAlgorithmChart
      do @renderRobotChart
      @

    renderAlgorithmChart: ->
      $el = @$ '.algorithm'
      $el.html @algorithmChart.render().el

    renderRobotChart: ->
      $el = @$ '.robot'
      $el.html @robotChart.render().el
