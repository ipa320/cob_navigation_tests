define [ 'backbone', 'templates/sortingOptions' ], ( Backbone, sortingOptionsTmpl )->
  Backbone.View.extend
    events:
      'click  input.sort': 'sortingChanged'
      'change #showErrorsChkbx': 'showErrorsChanged'

    render: ->
      filter = @model.get 'erroneousFilter'
      @$el.html sortingOptionsTmpl
        sorting:    @model.get 'sorting'
        showErrors: filter?.get 'show'
      @

    sortingChanged: ( e )->
      input = $ e.currentTarget
      value = do input.val
      @model.set 'sorting', value if value

    showErrorsChanged: ( e )->
      input  = $ e.currentTarget
      value  = input.prop 'checked'
      filter = @model.get 'erroneousFilter'
      filter?.set( 'show', value )
