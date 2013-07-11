define [ 'backbone' ], ( Backbone )->
  Backbone.Model.extend
    defaults:
      field: ''
      type:  'includes'
      value: ''
      link:  ''

    complies: ( number, test )->
      return null if !@get 'value'
      fieldsOfInterest = @getFieldsOfInterest test
      comparator = do @getComparator
      return comparator.call @, fieldsOfInterest

    getFieldsOfInterest: ( test )->
      robot      = test.get 'robot'
      navigation = test.get 'navigation'
      scenario  = test.get 'scenario'

      switch @get 'field'
        when 'any'        then [ robot, navigation, scenario ]
        when 'robot'      then [ robot ]
        when 'navigation' then [ navigation ]
        when 'scenario'  then [ scenario ]
        else
          console.warn 'Invalid filter field', @get 'field'
          []

    getComparator: ->
      type = @get 'type'
      if type == 'includes'
        return @includesComparator
      if type == 'excludes'
        return @excludesComparator
      return false

    includesComparator: ( fields )->
      value = @get 'value'
      for field in fields
        return true if field.indexOf( value ) > -1
      return false

    excludesComparator: ( fields )->
      value = @get 'value'
      for field in fields
        return false if field.indexOf( value ) > -1
      return true
