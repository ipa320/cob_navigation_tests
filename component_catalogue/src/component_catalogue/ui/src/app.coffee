define [ 'collections/textFilter', 'collections/tests', 'views/resultList', 'views/devView', 'models/testGroup', 'collections/testGroups',  'models/dateFilter', 'models/numberFilter', 'models/erroneousFilter', 'views/filterView', 'views/videoPlayback', 'views/sortingOptions', 'models/sortingOptions'  ], ( TextFilter, Tests, ResultList, DevView, TestGroup, TestGroups, DateFilter, NumberFilter, ErroneousFilter, FilterView, VideoPlayback, SortingOptionsView, SortingOptions )->

  ( options )->
    testCollection  = new Tests( options.testData ) # find better names for testCollection and tests
    textFilter      = new TextFilter
    dateFilter      = new DateFilter
    numberFilter    = new NumberFilter tests: testCollection
    erroneousFilter = new ErroneousFilter
    sortingOptions  = new SortingOptions
      erroneousFilter: erroneousFilter


    filters = [ textFilter, dateFilter, numberFilter, erroneousFilter ]

    tests = new TestGroup tests: testCollection, filters: filters
    groupedTests = tests.groupBy [ 'robot', 'navigation', 'scenario' ]
    testGroups   = new TestGroups groupedTests

    resultListView = null
    devView        = null

    renderResultListView = ->
      videoOverlay   = new VideoPlayback
      $( 'body' ).prepend videoOverlay.render().el
      resultListView = new ResultList
        testGroups:    testGroups
        videoPlayback: videoOverlay
      resultListView.on 'expandTestGroup', ( testGroup )->
        devView.activateTestDetailView testGroup

      $( '#resultListView' ).html resultListView.render().el

    renderDevView = ->
      devView = new DevView
        testGroups:     testGroups
        sortingOptions: sortingOptions
      devView.on 'changeView', ( view )->
        switch view
          when 'application' then resultListView.setSelectionMode 'promiscuous'
          when 'component'   then resultListView.setSelectionMode 'exclusive'
        _.defer -> $( window ).trigger( 'resize' )
      $( '#devView' ).html devView.render().el


    renderSortingOptionsView = ->
      sortingOptions = new SortingOptionsView
        model: sortingOptions
      @$( '#sortingOptionsContainer' ).html sortingOptions.render().el


    renderFilterView = ->
      filterView = new FilterView
        textFilter:   textFilter
        dateFilter:   dateFilter
        numberFilter: numberFilter
      $( '#filterView' ).html filterView.render().el


    $ ->
      do renderResultListView
      do renderFilterView
      do renderDevView
      do renderSortingOptionsView
      #$( '#top' ).splitter()
