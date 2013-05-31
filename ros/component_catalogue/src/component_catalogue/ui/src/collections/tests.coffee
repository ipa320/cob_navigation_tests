define [ 'underscore', 'backbone', 'models/test' ], ( _, Backbone, Test )->
  Tests = Backbone.Collection.extend
    model: Test

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

    filter: ( filters )->
      filtered      = new Tests
      compliedCount = 0
      for model in @models
        if @allFiltersComply compliedCount, model, filters
          filtered.add model, silent: true
          compliedCount++
      filtered

    allFiltersComply: ( number, model, filters )->
      for filter in filters
        if !filter.complies number, model
          return false
      true


    getIndexesByCid: ->
      indexesByCid = {}
      for index, model of @models
        indexesByCid[ model.cid ] = index
      return indexesByCid
