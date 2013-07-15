define [ 'underscore', 'backbone', 'models/test' ], ( _, Backbone, Test )->
  Tests = Backbone.Collection.extend
    model: Test
    comparator: 'localtime'

    groupBy: ( groups )->
      groupedSiblings = {}
      groupKey = ( model )->
        key = ''
        for group in groups
          key += model.get group
        key

      for model in @models
        key = groupKey model
        siblings = groupedSiblings[ key ] || ( groupedSiblings[ key ] = [] )
        siblings.push model

      _( groupedSiblings ).values().map ( models )->
        new Tests models


    getIndexesByCid: ->
      indexesByCid = {}
      for index, model of @models
        indexesByCid[ model.cid ] = index
      return indexesByCid

    applyFilters: ( filters )->
      for model in @models
        model.applyFilters filters
