define [ 'backbone', 'templates/sortingOptions' ], ( Backbone, sortingOptionsTmpl )->
  Backbone.View.extend
    events:
      'click  input.sort': 'sortingChanged'
      'change #showErrorsChkbx': 'showErrorsChanged'

    render: ->
      @$el.html sortingOptionsTmpl
        sorting:    @model.get 'sorting'
        showErrors: @model.get 'showErrors'
      @

    sortingChanged: ( e )->
      input = $ e.currentTarget
      value = do input.val
      @model.set 'sorting', value if value

    showErrorsChanged: ( e )->
      input = $ e.currentTarget
      value = input.prop 'checked'
      @model.set 'showErrors', value
