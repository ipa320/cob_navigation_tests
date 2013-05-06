define [ 'backbone', 'templates/sortingOptions' ], ( Backbone, sortingOptionsTmpl )->
  Backbone.View.extend
    events:
      'click input': 'sortingChanged'

    render: ->
      @$el.html sortingOptionsTmpl
        sorting: @model.get 'sorting'
      @

    sortingChanged: ( e )->
      input = $ e.currentTarget
      value = do input.val
      @model.set 'sorting', value if value
