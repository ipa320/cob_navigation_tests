define [ 'collections/testSeriesList', 'views/resultList' ], ( TestSeriesList, ResultList )->

  testSeries = new TestSeriesList testData
  $ ->
    resultListView = new ResultList({ collection: testSeries });
    $( '#app' ).html resultListView.render().el
