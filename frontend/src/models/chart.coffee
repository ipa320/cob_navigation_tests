define [ 'backbone'  ], ( Backbone )->

  Backbone.Model.extend
    defaults:
      key: ''
      title: ''
      xAxisCategories: null
      yAxisLabel: ''
      valueSuffix: ''

    initialize: ->
      @attributes.groups?.bind 'select', @groupSelected, this
      @attributes.groups?.bind 'unselect', @groupUnselected, this
      
    groupSelected: ( model )->
      hcSeries = @testGroupToHighchartSeries model
      this.trigger 'addSeries', hcSeries

    groupUnselected: ( model )->
      hcSeries = @testGroupToHighchartSeries model
      this.trigger 'removeSeries', hcSeries

    testGroupToHighchartSeries: ( model )->
      nameChunks = []
      for key in [ 'robot', 'algorithm', 'scenario' ]
        nameChunks.push model.get key

      date = model.getDataPointsForKey( 'date' )
      data = model.getDataPointsForKey( @attributes.key )
      name:  nameChunks.join ' / '
      id:    model.id
      data:  _.zip date, data


    highchartsConfig: ->
      series: []
      #chart:
        #type: 'line',
        #marginRight: 130
        #marginBottom: 25
      #title:
        #text: @attributes.title
      #xAxis:
        #categories: @attributes.xAxisCategories?
        #tickInterval: 1
      #yAxis:
        #title:
          #text: @attributes.yAxisLabel
        #plotLines: [
          #value: 0, width: 1, color: '#808080'
        #]
      #tooltip:
        #valueSuffix: @attributes.valueSuffix
      #legend:
        #layout: 'vertical',
        #align: 'right',
        #verticalAlign: 'top',
        #x: -10,
        #y: 100,
        #borderWidth: 0
      credits:
        enabled: false
      #series: []
      #series: [{
        #name: 'Tokyo',
        #data: [7.0, 6.9, 9.5, 14.5, 18.2, 21.5, 25.2, 26.5, 23.3, 18.3, 13.9, 9.6],
      #}]
