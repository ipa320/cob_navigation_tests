define [ 'backbone', 'templates/resultList' ], ( Backbone, resultListTmpl, fixedHeaderTable )->

  ResultList  = Backbone.View.extend
    id: 'resultList',
    tagName: 'div',
    events:
      'click table tr': 'selectRow'

    options:
      testGroups: null
      columns:
        'count':          '#'
        'robot':          'Roboter'
        'algorithm':      'Alogrithm'
        'scenario':       'Scenario'
        'mean.duration':  'Duration (&empty; in s)'
        'mean.distance':  'Distance (&empty; in m)'
        'mean.rotation':  'Rotation (&empty; in deg)'

    render: ->
      data = do @options.testGroups.toJSON
      data = data.filter ( row )-> row.count > 0

      table = $ resultListTmpl
        columns: @options.columns
        data: data
      @$el.html table
      #table.dataTable().appendTo( this.$el )
      this

    initialize: ->
      @listenTo @options.testGroups, 'change:enabled',  @enableChanged.bind @
      @listenTo @options.testGroups, 'change:count',    @refreshTable.bind @

    refreshTable: ->
      do @render

    enableChanged: ( model, enabled )->
      id = model.get 'id'
      @$( '#' + id ).toggleClass 'disabled', !enabled

    selectRow: ( e ) ->
      current = $( e.currentTarget )
      id = current.attr 'id'
      model = @options.testGroups.get id
      if model?.get 'enabled'
        current.toggleClass 'row_selected'
        selected = current.hasClass 'row_selected'
        model?.set 'selected', selected
