define [ 'collections/textFilter', 'collections/tests', 'views/resultList', 'views/devView', 'models/testGroup', 'collections/testGroups',  'models/dateFilter', 'models/numberFilter', 'views/filterView' ], ( TextFilter, Tests, ResultList, DevView, TestGroup, TestGroups, DateFilter, NumberFilter, FilterView )->

  tests = new TestGroup tests: new Tests testData
  textFilter   = new TextFilter
  dateFilter   = new DateFilter
  numberFilter = new NumberFilter
  filters = [ textFilter, dateFilter, numberFilter ]

  groupedTests = tests.groupBy [ 'robot', 'algorithm', 'scenario' ]
  testGroups = new TestGroups groupedTests, filters: filters


  #disableAllTestGroupsWithDifferentScenario = ( scenario )->
    #testGroups.forEach ( testGroup )->
      #if testGroup.get( 'scenario' ) != scenario
        #testGroup.set 'enabled', false

  #noTestGroupSelected = ->
    #noneSelected = true
    #testGroups.forEach ( testGroup )->
      #if testGroup.get 'selected'
        #noneSelected = false
    #return noneSelected

  #enableAllTestGroups = ->
    #testGroups.forEach ( testGroup )->
      #testGroup.set 'enabled', true

  #testGroups.on 'change:selected', ( testGroup, selected )->
    #if selected
      #disableAllTestGroupsWithDifferentScenario testGroup.get 'scenario'
    #else if do noTestGroupSelected
      #do enableAllTestGroups

  renderResultListView = ->
    resultListView = new ResultList testGroups: testGroups
    $( '#resultListView' ).html resultListView.render().el
    $(  '.exc' ).change ->
      exclusive = !$( this ).is( ':checked' )
      if exclusive
        resultListView.setSelectionMode 'exclusive'
      else
        resultListView.setSelectionMode 'promiscuous'

  renderDevView = ->
    devView = new DevView testGroups: testGroups
    $( '#devView' ).html devView.render().el


  renderFilterView = ->
    filterView = new FilterView
      textFilter:   textFilter
      dateFilter:   dateFilter
      numberFilter: numberFilter
    $( '#filterView' ).html filterView.render().el



  renderApplicationDeveloperCharts = ->
    appDevChartModels = [
      new ColumnChart
        key: 'rotation', yAxisLabel: 'Rotation in deg', valueSuffix: 'deg'
        title: 'Rotation', groups: testGroups, filter: filter
    ]

    appDevChartContainer = $( '#applicationCharts' )
    containers = []
    for chartModel in appDevChartModels
      c = $( '<div class="chart-container" />' ).appendTo appDevChartContainer
      containers.push c

    for i, chartModel of appDevChartModels
      c = containers[ i  ]
      chart = new ApplicationChart model: chartModel
      c.html chart.render( c.width() ).el

  $ ->
    #do renderComponentDeveloperCharts
    #do renderApplicationDeveloperCharts
    do renderResultListView
    do renderFilterView
    do renderDevView
    $( '.exc' ).prop( 'checked', false ).trigger( 'change' )
    #setTimeout ( -> $( window ).trigger( 'resize' )), 0
