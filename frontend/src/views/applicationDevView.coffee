define [ 'backbone', 'templates/applicationDev', 'views/applicationDevChart' ], ( Backbone, applicationDevTmpl, ApplicationDevChart )->
  Backbone.View.extend
    tagName:   'div'
    className: 'applicationDevView'

    render: ->
      @$el.html do applicationDevTmpl
      do @renderAlgorithmChart
      do @renderRobotChart
      @

    renderAlgorithmChart: ->
      view = new ApplicationDevChart
        testGroups:           @options.testGroups
        variableAttributeKey: 'algorithm'
        fixedAttributeKeys:   [ 'robot', 'scenario' ]

      $el = @$ '.algorithm'
      $el.html view.render().el
      

    renderRobotChart: ->
      view = new ApplicationDevChart
        testGroups:           @options.testGroups
        variableAttributeKey: 'robot'
        fixedAttributeKeys:   [ 'algorithm', 'scenario' ]

      $el = @$ '.robot'
      $el.html view.render().el
