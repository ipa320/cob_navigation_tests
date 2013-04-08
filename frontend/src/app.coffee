define [ 'collections/testSeries', 'views/resultList', 'views/developerChart', 'models/chart', 'models/testSeriesFiltered' ], ( TestSeries, ResultList, DeveloperChart, Chart, TestSeriesFiltered )->

  testSeries = new TestSeries testData
  $ ->
    devChartModels = [
      new Chart 
        key: 'duration', yAxisLabel: 'Duration in s', valueSuffix: 's'
        title: 'Duration', series: testSeries
      new Chart 
        key: 'distance', yAxisLabel: 'Distance in m', valueSuffix: 'm'
        title: 'Distance', series: testSeries
      new Chart 
        key: 'rotation', yAxisLabel: 'Rotation in deg', valueSuffix: 'deg'
        title: 'Rotation', series: testSeries
    ]

    filtered = new TestSeriesFiltered series: testSeries
    rows = new Backbone.Collection [ ]
    rows.add filtered.filter robot: 'cob3-3'

    console.log rows
    resultListView = new ResultList model: rows

    #developerChartsContainer = $( '#developerCharts' )
    #for chartModel in devChartModels
      #chart = new DeveloperChart model: chartModel
      #developerChartsContainer.append chart.render().el

    $( '#resultListView' ).html resultListView.render().el
