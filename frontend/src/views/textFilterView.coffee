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

    selectPrevious: ( view )->
      @select view, 'prev'

    selectNext: ( view )->
      @select view, 'next'

    select: ( view, target )->
      $row       = $ view?.el
      $target    = do $row[ target ]
      targetView = $target.data 'view'
      do targetView.focus if targetView

    addNewRow: ->
      criteria = new TextFilterCriteria
      newView  = new TextFilterRow model: criteria
      @listenTo newView, 'escape',         @escape.bind         @, newView, criteria
      @listenTo newView, 'selectNext',     @selectNext.bind     @, newView
      @listenTo newView, 'selectPrevious', @selectPrevious.bind @, newView
      @listenTo newView, 'andClicked',     @addNewRow.bind      @, criteria
      @listenTo newView, 'orClicked',      @addNewRow.bind      @, criteria

      @options.textFilter.add criteria
      $row = newView.render().$el
      console.log newView, newView.el
      $row.data 'view', newView

      @$( '.rows' ).append $row
      do newView.focus
