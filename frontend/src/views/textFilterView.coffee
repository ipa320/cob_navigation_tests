define [ 'backbone', 'views/textFilterRow', 'templates/textFilter', 'models/textFilterCriteria' ], ( Backbone, TextFilterRow, textFilterTmpl, TextFilterCriteria )->
  TextFilterView = Backbone.View.extend
    tagName: 'div'
    className: 'textFilter'
    events:
      'click .or, .and':  'addNewRow'

    render: ->
      do @addNewRow
      this

    addNewRow: ->
      criteria = new TextFilterCriteria
      newRow = new TextFilterRow criteria: criteria
      @options.textFilter.add criteria
      @$el.append newRow.render().el
