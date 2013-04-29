define [ 'backbone', 'templates/devView', 'views/componentDevView', 'views/applicationDevView' ], ( Backbone, devViewTmpl, ComponentDevView, ApplicationDevView )->
  Backbone.View.extend
    tagName:   'div'
    className: 'developerView'

    render: ->
      @$el.html do devViewTmpl
      #@renderComponentDevView   @$ '.componentDevView'
      @renderApplicationDevView @$ '.applicationDevView'
      @

    renderComponentDevView: ( $el )->
      componentDevView = new ComponentDevView testGroups: @options.testGroups
      $el.html componentDevView.render().el

    renderApplicationDevView: ( $el )->
      applicationDevView = new ApplicationDevView testGroups: @options.testGroups
      $el.html applicationDevView.render().el
