define [ 'backbone', 'views/textFilterRow', 'templates/textFilter', 'models/textFilterCriteria' ], ( Backbone, TextFilterRow, textFilterTmpl, TextFilterCriteria )->
  TextFilterView = Backbone.View.extend
    tagName:   'div'
    className: 'textFilter'

    initialize: ->
      @rowViews = []

    escape: ( view, criteria )->
      $row  = $ view.el
      $prev = do $row.prev
      if $prev.length
        @stopListening view
        do $prev.data( 'view' ).focus
        $row.data 'view', null
        do view.remove
        @options.textFilter.remove criteria
        do @removeLinkFromLastCriteria
      else
        do view.clear

    removeLinkFromLastCriteria: ->
      @options.textFilter.last().set 'link', ''

    render: ->
      @$el.html do textFilterTmpl
      do @addNewRow
      this

    addNewRow: ->
      criteria = new TextFilterCriteria
      newView = new TextFilterRow model: criteria
      @listenTo newView, 'escape', @escape.bind @, newView, criteria
      @listenTo newView, 'andClicked', @addNewRow.bind @, criteria
      @listenTo newView, 'orClicked',  @addNewRow.bind  @, criteria

      @options.textFilter.add criteria
      $row = newView.render().$el
      $row.data 'view', newView

      @$( '.rows' ).append $row
      do newView.focus
