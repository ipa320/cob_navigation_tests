define [ 'templates/filter', 'views/dateFilterView', 'views/textFilterView', 'views/numberFilterView' ], ( filterTmpl, DateFilterView, TextFilterView, NumberFilterView )->

  Backbone.View.extend
    tagName:   'div'
    className: 'filterView'

    render: ->
      @$el.html do filterTmpl
      @renderTextFilterView @$( '.textFilterContainer' )
      @renderDateFilterView @$( '.dateFilterContainer' )
      @renderNumberFilterView @$( '.numberFilterContainer' )
      @

    renderTextFilterView: ( $el )->
      textFilterView = new TextFilterView textFilter: @options.textFilter
      $el.html textFilterView.render().el

    renderDateFilterView: ( $el )->
      dateFilterView = new DateFilterView dateFilter: @options.dateFilter
      $el.append dateFilterView.render().el

    renderNumberFilterView: ( $el )->
      numberFilterView = new NumberFilterView numberFilter: @options.numberFilter
      $el.append numberFilterView.render().el
