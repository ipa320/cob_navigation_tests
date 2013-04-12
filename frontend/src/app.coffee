define [ 'collections/tests', 'views/resultList', 'views/developerChart', 'models/chart', 'collections/testGroups' ], ( Tests, ResultList, DeveloperChart, Chart, TestGroups )->

  tests = new Tests testData
  groupedTests = tests.groupBy [ 'robot', 'algorithm', 'scenario' ]
  testGroups = new TestGroups groupedTests

  $ ->
    devChartModels = [
      new Chart
        key: 'duration', yAxisLabel: 'Duration in s', valueSuffix: 's'
        title: 'Duration', groups: testGroups
      new Chart
        key: 'distance', yAxisLabel: 'Distance in m', valueSuffix: 'm'
        title: 'Distance', groups: testGroups
      new Chart
        key: 'rotation', yAxisLabel: 'Rotation in deg', valueSuffix: 'deg'
        title: 'Rotation', groups: testGroups
    ]

    #filtered = new TestSeriesFiltered series: testSeries
    #rows = new Backbone.Collection [ ]
    #rows.add filtered.filter robot: 'cob3-3'

    #console.log rows
    resultListView = new ResultList testGroups: testGroups

    developerChartsContainer = $( '#developerCharts' )
    for chartModel in devChartModels
      chart = new DeveloperChart model: chartModel
      developerChartsContainer.append chart.render().el

    $( '#resultListView' ).html resultListView.render().el
