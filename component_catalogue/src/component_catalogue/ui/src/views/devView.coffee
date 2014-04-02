define [ 'backbone', 'templates/devView', 'views/componentDevView', 'views/applicationDevView', 'views/testDetailDevView' ], ( Backbone, devViewTmpl, ComponentDevView, ApplicationDevView, TestDetailDevView )->
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

      @testDetailDevView = new TestDetailDevView
        testGroups:     @options.testGroups

    renderComponentDevView: ( $el )->
      $el.html @componentDevView.render().el
      $( '#sortingOptionsContainer' ).show()

    renderApplicationDevView: ( $el )->
      $el.html @applicationDevView.render().el
      $( '#sortingOptionsContainer' ).hide()

    renderTestDetailDevView: ( $el )->
      $el.html @testDetailDevView.render().el
      $( '#sortingOptionsContainer' ).hide()

    activateTestDetailView: ( testGroup )->
      @testDetailDevView.useTestGroup testGroup
      @trigger 'changeView', 'testDetail'
      @renderTestDetailDevView @$ '.tabContent'

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
