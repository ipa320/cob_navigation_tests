define [ 'backbone', 'templates/applicationDev', 'views/applicationDevChart' ], ( Backbone, applicationDevTmpl, ApplicationDevChart )->
  Backbone.View.extend
    tagName:   'div'
    className: 'applicationDev'

    render: ->
      @$el.html do applicationDevTmpl
      do @renderAlgorithmChart
      #do @renderRobotChart
      @

    renderAlgorithmChart: ->
      view = new ApplicationDevChart
        testGroups:           @options.testGroups
        variableAtributteKey: 'algorithm'
        fixedAttributeKeys:   [ 'robot', 'scenario' ]

      $el = @$ '.algorithm'
      $el.html view.render().el
