define [ 'backbone', 'views/textFilterRow', 'templates/textFilter', 'models/textFilterCriteria' ], ( Backbone, TextFilterRow, textFilterTmpl, TextFilterCriteria )->
  TextFilterView = Backbone.View.extend
    tagName:   'div'
    className: 'textFilter'
    events:
      'click .or, .and':  'addNewRow'

    initialize: ->
      @rowViews = []

    escape: ( row, criteria )->
      do row.remove
      @options.textFilter.remove criteria
      do @removeLinkFromLastCriteria

    removeLinkFromLastCriteria: ->
      @options.textFilter.last().set 'link', ''

    render: ->
      @addNewRow false
      this

    addNewRow: ( removable=true )->
      criteria = new TextFilterCriteria
      newRow = new TextFilterRow model: criteria
      if removable
        @listenTo newRow, 'escape', @escape.bind @, newRow, criteria
      @options.textFilter.add criteria
      @$el.append newRow.render().el
      do newRow.focus
