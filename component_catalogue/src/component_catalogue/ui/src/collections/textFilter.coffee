define [ 'backbone', 'models/textFilterCriteria' ], ( Backbone, TextFilterCriteria )->
  Backbone.Collection.extend
    model: TextFilterCriteria

    complies: ( number, test )->
      result = @evaluate number, test, 0
      return true if result == null
      return result

    evaluate: ( number, test, index )->
      criteria = @models[ index ]
      return null if !criteria
      result = criteria.complies number, test
      link   = criteria.get 'link'
      return null if result == null

      nextResult = @evaluate number, test, index+1
      if link == 'and'
        return result if nextResult == null
        return result && nextResult
      if link == 'or'
        return result == true || nextResult == true
      return result
