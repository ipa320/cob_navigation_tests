define [ 'collections/textFilter', 'collections/tests', 'views/resultList', 'views/devView', 'models/testGroup', 'collections/testGroups',  'models/dateFilter', 'models/numberFilter', 'views/filterView', 'views/videoPlayback' ], ( TextFilter, Tests, ResultList, DevView, TestGroup, TestGroups, DateFilter, NumberFilter, FilterView, VideoPlayback )->

  ( options )->
    testCollection = new Tests( options.testData ) # find better names for testCollection and tests
    textFilter     = new TextFilter
    dateFilter     = new DateFilter
    numberFilter   = new NumberFilter tests: testCollection


    filters = [ textFilter, dateFilter, numberFilter ]

    tests = new TestGroup tests: testCollection, filters: filters
    groupedTests = tests.groupBy [ 'robot', 'navigation', 'scenario' ]
    testGroups   = new TestGroups groupedTests

    resultListView = null

    renderResultListView = ->
      resultListView = new ResultList testGroups: testGroups
      $( '#resultListView' ).html resultListView.render().el

    renderDevView = ->
      devView = new DevView testGroups: testGroups
      devView.on 'changeView', ( view )->
        switch view
          when 'application' then resultListView.setSelectionMode 'promiscuous'
          when 'component'   then resultListView.setSelectionMode 'exclusive'
        _.defer -> $( window ).trigger( 'resize' )
      $( '#devView' ).html devView.render().el


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
      #$( '#top' ).splitter()
