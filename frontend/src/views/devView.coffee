define [ 'backbone', 'templates/devView', 'views/componentDevView', 'views/applicationDevView' ], ( Backbone, devViewTmpl, ComponentDevView, ApplicationDevView )->
  Backbone.View.extend
    tagName:   'div'
    className: 'developerView'
    events:
      'click .tab.component':   "activateComponentView"
      'click .tab.application': "activateApplicationView"

    render: ->
      @$el.html do devViewTmpl
      do @activateApplicationView
      @

    renderComponentDevView: ( $el )->
      componentDevView = new ComponentDevView testGroups: @options.testGroups
      $el.html componentDevView.render().el

    renderApplicationDevView: ( $el )->
      applicationDevView = new ApplicationDevView testGroups: @options.testGroups
      $el.html applicationDevView.render().el

    activateApplicationView: ->
      @activateTab 'application'
      @trigger 'changeView', 'application'
      @renderApplicationDevView @$ '.tabContent'

    activateComponentView: ->
      @trigger 'changeView', 'component'
      @activateTab 'component'
      @renderComponentDevView @$ '.tabContent'

    activateTab: ( name )->
      @$( '.tab.active' ).removeClass 'active'
      @$( '.tab.' + name ).addClass 'active'
