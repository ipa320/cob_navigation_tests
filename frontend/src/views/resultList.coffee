define [ 'templates/resultList', 'collections/testSeriesList', 'jquery.dataTables' ], ( resultListTmpl, TestSeriesList, dataTables )->

  ResultList  = Backbone.View.extend
    id: 'list',
    tagName: 'div',
    events:
      'click table tr': 'selectRow'

    options:
      columns:
        'date':           'Date'
        'robot':          'Roboter'
        'algorithm':      'Alogrithm'
        'scenario':       'Scenario'
        'mean.duration':  'Duration (&empty; in s)'
        'mean.distance':  'Distance (&empty; in m)'
        'mean.rotation':  'Rotation (&empty; in deg)'

    render: ->
      table = $ resultListTmpl
        columns: @options.columns
        data: do @options.collection.toAnalyzedJSON
      table.dataTable().appendTo( this.$el )
      this

    initialize: ->
      @selectedRows = new TestSeriesList

    selectRow: ( e ) ->
      current = $( e.currentTarget )
      current.toggleClass 'row_selected'
      id = +current.data 'id'
      model = @options.collection.get id
      return if not model
      if @selectedRows.get id
        @selectedRows.remove id
      else
        @selectedRows.add model
      console.log 'selected rows', @selectedRows
