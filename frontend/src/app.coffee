define [ 'collections/tests', 'views/resultList', 'views/developerChart', 'views/applicationChart', 'models/lineChart', 'views/dateFilterView', 'models/columnChart', 'models/testGroup', 'collections/testGroups', 'collections/textFilter', 'models/dateFilter', 'views/textFilterView', 'models/numberFilter', 'views/numberFilterView' ], ( Tests, ResultList, DeveloperChart, ApplicationChart, LineChart, DateFilterView, ColumnChart, TestGroup, TestGroups, TextFilter, DateFilter, TextFilterView, NumberFilter, NumberFilterView )->

  tests = new TestGroup tests: new Tests testData
  textFilter   = new TextFilter
  dateFilter   = new DateFilter
  numberFilter = new NumberFilter

  groupedTests = tests.groupBy [ 'robot', 'algorithm', 'scenario' ]
  testGroups = new TestGroups \
    groupedTests, \
    textFilter: textFilter, dateFilter: dateFilter, numberFilter: numberFilter

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

  renderTextFilterView = ->
    textFilterView = new TextFilterView textFilter: textFilter
    $( 'body' ).append textFilterView.render().el

  renderResultListView = ->
    resultListView = new ResultList testGroups: testGroups
    $( '#resultListView' ).html resultListView.render().el

  renderDateFilterView = ->
    dateFilterView = new DateFilterView dateFilter: dateFilter
    $( 'body' ).append dateFilterView.render().el

  renderNumberFilterView = ->
    numberFilterView = new NumberFilterView numberFilter: numberFilter
    $( 'body' ).append numberFilterView.render().el

  renderComponentDeveloperCharts = ->
    devChartModels = [
      new LineChart
        key: 'duration', yAxisLabel: 'Duration in s', valueSuffix: 's'
        title: 'Duration', groups: testGroups, filter: textFilter
      new LineChart
        key: 'distance', yAxisLabel: 'Distance in m', valueSuffix: 'm'
        title: 'Distance', groups: testGroups, filter: textFilter
      new LineChart
        key: 'rotation', yAxisLabel: 'Rotation in deg', valueSuffix: 'deg'
        title: 'Rotation', groups: testGroups, filter: filter
    ]
    componentChartsContainer = $( '#componentCharts' )
    containers = []
    for chartModel in devChartModels
      c = $( '<div class="chart-container" />' ).appendTo componentChartsContainer
      containers.push c

    for i, chartModel of devChartModels
      c = containers[ i ]
      chart = new DeveloperChart model: chartModel
      c.html chart.render( c.width() ).el


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
    do renderTextFilterView
    do renderDateFilterView
    do renderNumberFilterView
