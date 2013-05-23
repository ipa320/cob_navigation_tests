define [ 'backbone', 'templates/applicationDev', 'views/applicationDevChart' ], ( Backbone, applicationDevTmpl, ApplicationDevChart )->
  Backbone.View.extend
    tagName:   'div'
    className: 'applicationDevView'

    initialize: ->
      @navigationChart = new ApplicationDevChart
        testGroups:           @options.testGroups
        variableAttributeKey: 'navigation'
        fixedAttributeKeys:   [ 'robot', 'scenario' ]
        title: 'Different Navigations for fixed robot and scenario'

      @robotChart = new ApplicationDevChart
        testGroups:           @options.testGroups
        variableAttributeKey: 'robot'
        fixedAttributeKeys:   [ 'navigation', 'scenario' ]
        title: 'Different robots for fixed navigations and scenario'

    render: ->
      @$el.html do applicationDevTmpl
      do @renderNavigationChart
      do @renderRobotChart
      @

    renderNavigationChart: ->
      $el = @$ '.navigation'
      $el.html @navigationChart.render().el

    renderRobotChart: ->
      $el = @$ '.robot'
      $el.html @robotChart.render().el
