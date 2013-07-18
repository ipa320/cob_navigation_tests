define [ 'backbone', 'jquery-tipTip', 'jquery.dataTables', 'templates/resultList', 'templates/resultDetailList', 'views/columnsResultList', 'views/columnsDetailResultList' ], ( Backbone, tiptip, dataTables, resultListTmpl, resultDetailListTmpl, columnsResultList, columnsDetailResultList )->

  ResultList  = Backbone.View.extend
    id: 'resultList',
    tagName: 'div',
    events:
      #'click table tr': 'selectRow'
      'click input':      'changeSelected'
      'click tr':         'triggerInputClick'
      'click td.zoom':    'toggleRow'
      'click td.video a': 'playVideo'
      'click a.back':     'backToGroups'

    options:
      testGroups:    null
      columns:       columnsResultList
      columnsDetail: columnsDetailResultList

    render: ->
      data = do @options.testGroups.toJSON
      data = data.filter ( row )-> row.count > 0

      table = $ resultListTmpl
        columns: @options.columns
        data: data
      @$el.html table
      @enhanceTable table, [[ 10, 'asc' ], [ 9, 'asc' ], [ 11, 'asc' ]]

      this

    enhanceTable: _.debounce ( table, sorting=[] )=>
      height = table.find( 'table' ).parent().height() - 50
      table.find( 'table' ).dataTable
        'sScrollY':        "#{height}px"
        'bPaginate':       false
        'bScrollCollapse': true
        'bSortCellsTop':   true
      table.find( 'th' ).tipTip
        defaultPosition: 'left'
    , 50

    initialize: ->
      @listenTo @options.testGroups, 'change:enabled', @enableChanged
      @listenTo @options.testGroups, 'change:count',   @refreshTable
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

    toggleRow: ( e )->
      e.preventDefault()
      e.stopImmediatePropagation()
      icon = $( e.currentTarget ).find '.icon'
      row  = $( e.currentTarget ).closest '.row'
      id   = row.attr 'id'
      icon.toggleClass 'expanded contracted'
      testGroup = @options.testGroups.get id
      @expandTestGroup testGroup

    expandTestGroup: ( testGroup )->
      row = @$ '#' + testGroup.id
      @$el.children().hide()
      detailTable = $ resultDetailListTmpl
        # change naming convention, totally confusing
        title:         testGroup.get 'title'
        columns:       @options.columnsDetail
        columnsDetail: @options.columnsDetail
        detail:  do testGroup.toJSON
        data:    do testGroup.get( 'tests' ).toJSON
      @enhanceTable detailTable, [[ 0, 'asc' ]]
      @$el.prepend detailTable

    playVideo: ( e )->
      a   = $ e.currentTarget
      src = a.attr 'href'
      do e.preventDefault
      @options.videoPlayback.play src

    backToGroups: ( e )->
      do @$( '.details' ).remove
      do @$el.children().show
