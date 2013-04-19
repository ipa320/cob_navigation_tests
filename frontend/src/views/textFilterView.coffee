define [ 'backbone', 'views/textFilterRow', 'templates/textFilter', 'models/textFilterCriteria' ], ( Backbone, TextFilterRow, textFilterTmpl, TextFilterCriteria )->
  TextFilterView = Backbone.View.extend
    tagName: 'div'
    className: 'textFilter'
    events:
      'click .or, .and':  'addNewRow'

    initialize: ->
      console.log 'initialize', @options.textFilter
      @options.textFilter.on 'change', ->
        console.log 'changeee'

    escape: ( row, criteria )->
      console.log @options.textFilter.length
      do row.remove
      @options.textFilter.remove criteria
      console.log criteria
      console.log @options.textFilter.length

    render: ->
      @addNewRow false
      this

    addNewRow: ( removable=true )->
      criteria = new TextFilterCriteria
      newRow = new TextFilterRow criteria: criteria
      if removable
        @listenTo newRow, 'escape', @escape.bind @, newRow, criteria
      @options.textFilter.add criteria
      @$el.append newRow.render().el
      do newRow.focus
