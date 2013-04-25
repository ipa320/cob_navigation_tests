define [ 'backbone' ], ( Backbone )->
  Test = Backbone.Model.extend
    defaults:
      date: 0
      robot: ''
      scenario: ''
      algorithm: ''
      tooSexy: 'yes'
      testResults: null
      duration:  null
      distance:  null
      rotation:  null

    initialize: ->
      date = @get 'date'
      if !( date instanceof Date )
        @set 'date', new Date date

    complies: ( filters )->
      for name, filter of filters
        methodName = 'complies' + name[ 0 ].toUpperCase() + name[ 1.. ]
        if @[ methodName ]? and !@[ methodName ] filter
          return false
      return true

    compliesTextFilter: ( textFilter )->
      robot     = @get 'robot'
      algorithm = @get 'algorithm'
      scenario  = @get 'scenario'

      comparator = ( fields, value, type )->
        if value == ''
          return null
        if type == 'includes'
          return includesComparator fields, value
        if type == 'excludes'
          return excludesComparator fields, value
        return false

      includesComparator  = ( fields, value )->
        for field in fields
          return true if field.indexOf( value ) > -1
        return false

      excludesComparator = ( fields, value )->
        for field in fields
          return false if field.indexOf( value ) > -1
        return true

      affectedFields = ( field )->
        switch field
          when 'any'       then [ robot, algorithm, scenario ]
          when 'robot'     then [ robot ]
          when 'algorithm' then [ algorithm ]
          when 'scenario'  then [ scenario ]

      criterias = textFilter.models

      evaluate = ( index )->
        criteria = criterias[ index ]
        return null if not criteria
        value  = criteria.get 'value'
        type   = criteria.get 'type'
        link   = criteria.get 'link'
        field  = criteria.get 'field'
        fields = affectedFields field

        #if value == 'dwa'
          #console.log fields, value, type
          #throw 'he'
        result = comparator( fields, value, type )
        nextResult = evaluate index+1
        return result if result == null or nextResult == null

        if link == 'and'
          return result and nextResult
        if link == 'or'
          return result or nextResult
        return result

      result = evaluate 0
      return if result or result == null then true else false

    compliesDateFilter: ( dateFilter )->
      date  = @get 'date'
      start = dateFilter.get 'start'
      end   = dateFilter.get 'end'
      return ( !start || start <= date ) && ( !end || end >= date )

    compliesNumberFilter: ( numberFilter )->
      count = numberFilter.get 'count'
      compliedCount = @get 'compliedCount'
      return !compliedCount || !count || compliedCount < count
