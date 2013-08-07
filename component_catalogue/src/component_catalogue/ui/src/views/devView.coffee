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

    initialize: ->
      @applicationDevView = new ApplicationDevView
        testGroups:     @options.testGroups
        sortingOptions: @options.sortingOptions

      @componentDevView = new ComponentDevView
        testGroups:     @options.testGroups
        sortingOptions: @options.sortingOptions

    renderComponentDevView: ( $el )->
      $el.html @componentDevView.render().el
      $( '#sortingOptionsContainer' ).show()

    renderApplicationDevView: ( $el )->
      $el.html @applicationDevView.render().el
      $( '#sortingOptionsContainer' ).hide()

    activateApplicationView: ->
      if @activeTab() != 'application'
        @activateTab 'application'
        @trigger 'changeView', 'application'
        @renderApplicationDevView @$ '.tabContent'

    activateComponentView: ->
      if @activeTab() != 'component'
        @activateTab 'component'
        @trigger 'changeView', 'component'
        @renderComponentDevView @$ '.tabContent'

    activeTab: ->
      @activeTabName

    activateTab: ( name )->
      @$( '.tab.active' ).removeClass 'active'
      @$( '.tab.' + name ).addClass 'active'
      @activeTabName = name
