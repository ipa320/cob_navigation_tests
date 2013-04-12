define [ 'templates/resultList', 'jquery.dataTables' ], ( resultListTmpl, dataTables )->

  ResultList  = Backbone.View.extend
    id: 'list',
    tagName: 'div',
    events:
      'click table tr': 'selectRow'

    options:
      columns:
        'robot':     'Roboter'
        'algorithm': 'Alogrithm'
        'scenario':  'Scenario'
        'duration':  'Duration (&empty; in s)'
        'distance':  'Distance (&empty; in m)'
        'rotation':  'Rotation (&empty; in deg)'

    render: ->
      table = $ resultListTmpl
        columns: @options.columns
        data: do @options.testGroups.toJSON
      table.dataTable().appendTo( this.$el )
      this

    initialize: ->

    selectRow: ( e ) ->
      current = $( e.currentTarget )
      current.toggleClass 'row_selected'
      selected = current.hasClass 'row_selected'
      id = current.data 'id'
      model = @options.testGroups.get id
      console.log model.attributes
      model?.trigger selected && 'select' || 'unselect', model
