define [ 'backbone' ], ( Backbone )->
  Backbone.View.extend
    tagName:   'div'
    className: 'devChart'

    initialize: ->
      @listenTo @options.testGroups, 'change:empty change:selected', @groupsChanged

    render: ->
      @$el.html( 'oookay' )
      @

    groupsChanged: ->
      models = []
      @options.testGroups.each ( testGroup )=>
        if testGroup.get( 'selected' ) and !testGroup.get 'empty'
          models.push testGroup

      switch models.length
        when 0 then do @noItemSelected
        when 1 then do @oneItemSelected
        else do @multipleItemsSelected

    noItemSelected: ->
      @$el.html 'no item selected'

    oneItemSelected: ->
      @$el.html 'one item selected'

    multipleItemsSelected: ->
      @$el.html 'multiple items selected'
