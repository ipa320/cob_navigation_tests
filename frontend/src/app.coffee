define [ 'collections/textFilter', 'collections/tests', 'views/resultList', 'views/devView', 'models/testGroup', 'collections/testGroups',  'models/dateFilter', 'models/numberFilter', 'views/filterView' ], ( TextFilter, Tests, ResultList, DevView, TestGroup, TestGroups, DateFilter, NumberFilter, FilterView )->

  tests = new TestGroup tests: new Tests testData
  textFilter   = new TextFilter
  dateFilter   = new DateFilter
  numberFilter = new NumberFilter
  filters = [ textFilter, dateFilter, numberFilter ]

  groupedTests = tests.groupBy [ 'robot', 'algorithm', 'scenario' ]
  testGroups = new TestGroups groupedTests, filters: filters

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
