define [ 'templates/resultList', 'jquery.dataTables' ], ( resultListTmpl, dataTables )->

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
        data: do @model.toJSON
      table.dataTable().appendTo( this.$el )
      this

    initialize: ->

    selectRow: ( e ) ->
      current = $( e.currentTarget )
      current.toggleClass 'row_selected'
      selected = current.hasClass 'row_selected'
      id = +current.data 'id'
      model = @collection.get id 
      model?.trigger selected && 'select' || 'unselect', model 
