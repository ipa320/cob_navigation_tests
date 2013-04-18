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

    textFilter: ( textFilter )->
      filtered = new Tests
      for model in @models
        if model.complies textFilter
          filtered.add model, silent: true
      filtered
