define [ 'backbone', 'jquery-tipTip', 'templates/resultList' ], ( Backbone, tiptip, resultListTmpl, fixedHeaderTable )->

  ResultList  = Backbone.View.extend
    id: 'resultList',
    tagName: 'div',
    events:
      #'click table tr': 'selectRow'
      'click input':  'changeSelected'
      'click tr':     'triggerInputClick'

    options:
      testGroups: null
      columns:
        'count':           [ '#',          'Total number of tests' ]
        'errorsCombined':  [ '#ERR',       'Total number of all errors combined' ]
        'errorsAborted':   [ '#ABRTD',     'Error: Numer of times the navigation aborted, ' +
          'i.e. simple_action_client.get_state() returned ABORTED' ]
        'errorsFailed':    [ '#FLD',       'Error: Numer of times the navigation failed, ' +
          'i.e. simple_action_client.get_state() did neither return SUCCEEDED nor ABORTED' ]
        'errorsMissed':    [ '#MISS',      'Error: Number of time the navigation returned success ' +
          'but the actual position did not match the goal position' ]
        'errorsTimedout':  [ '#TO',        'Error: Number of times the navigation timed out' ]
        'mean.collisions': [ '#Col',       'Number of collisions' ]
        'robot':           [ 'Roboter',    'The robot used in the simulation' ]
        'navigation':      [ 'Navigation', 'The navigation used in the simulation' ]
        'scenario':        [ 'Scenario',   'The scenarion used in the simulation' ]
        'mean.duration':   [ 'Duration',   'Duration &empty; in s' ]
        'mean.distance':   [ 'Distance',   'Distance the robot moved &empty; in m' ]
        'mean.rotation':   [ 'Rotation',   'Number of degree the robot rotated &empty; in deg' ]

    render: ->
      data = do @options.testGroups.toJSON
      data = data.filter ( row )-> row.count > 0

      table = $ resultListTmpl
        columns: @options.columns
        data: data
      @$el.html table
      @$el.find( 'th div' ).tipTip()
      #table.dataTable().appendTo( this.$el )
      this

    initialize: ->
      @listenTo @options.testGroups, 'change:enabled',  @enableChanged.bind @
      @listenTo @options.testGroups, 'change:count',    @refreshTable.bind @
      @setSelectionMode @options.selectionMode

    refreshTable: ->
      do @render

    enableChanged: ( model, enabled )->
      id = model.get 'id'
      @$( '#' + id ).toggleClass 'disabled', !enabled

    changeSelected: ( e ) ->
      checkbox = $ e.currentTarget
      checked  = checkbox.is( ':checked' )
      row      = checkbox.closest '.row'
      id       = row.attr 'id'
      model    = @options.testGroups.get id

      model.set 'selected', checked
      if @options.selectionMode == 'exclusive' and checked
        @unselectAllGroups except: model

    setSelectionMode: ( mode )->
      mode = 'promiscuous' if mode not in [ 'exclusive', 'promiscuous' ]
      changed = mode != @options.selectionMode
      @options.selectionMode = mode
      return if not changed

      if mode == 'promiscuous'
        do @selectAllGroups
      else
        do @unselectAllGroups

    selectAllGroups: ->
      @options.testGroups.each ( testGroup )->
        testGroup.set 'selected', true
      do @updateCheckboxes

    unselectAllGroups: ( options )->
      @options.testGroups.each ( testGroup )->
        return if options?.except == testGroup
        testGroup.set 'selected', false
      do @updateCheckboxes

    updateCheckboxes: ->
      rows = @$ '.row'
      rows.each ( i, row )=>
        $row   = $ row
        id     = $row.attr 'id'
        model  = @options.testGroups.get id

        chkbox = $row.find 'input:first'
        chkbox.prop 'checked', model.get 'selected'

    triggerInputClick: ( e )->
      target = $ e.target
      return if target.is 'input'
      target.parent().find( 'input' ).trigger 'click'
