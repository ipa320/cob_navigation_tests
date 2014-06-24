define [ 'backbone' ], ( Backbone )->
  Backbone.Model.extend
    defaults:
      testGroup:       undefined
      hcSeries:        undefined
      key:             ''
      title:           ''
      xAxisCategories: null
      yAxisLabel:      ''
      valueSuffix:     ''
      filter:          null

    updateDeltas: ( t, deltas )->
      data = []
      for i in [ 0..t.length ]
        data.push [ parseInt( t[ i ]), deltas[ i ] ]
      hcSeries =
        name: 'test'
        data: data
      @set 'hcSeries', hcSeries
