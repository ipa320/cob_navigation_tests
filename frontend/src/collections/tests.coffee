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
        model.set 'compliedCount', compliedCount
        if model.complies filters
          filtered.add model, silent: true
          compliedCount++
      filtered
