define [ 'backbone', 'underscore', 'collections/tests' ], ( Backbone, _, Tests )->
  TestGroup = Backbone.Model.extend
    defaults:
      robot:      'None'
      robots:     [],
      scenario:   'None'
      scenarios:  [],
      algorithm:  'None'
      algorithms: []

    constructor: ( args, options )->
      if !(args?)
        args = tests: []
      if args instanceof Tests
        args = tests: args
      if !args.tests
        args.tests = []
      if args.tests && !( args.tests instanceof Tests )
        args.tests = new Tests args.tests
        
      if !( args.id )?
        args.id = _.uniqueId 'testGroup'
      Backbone.Model.call this, args, options
      this

    initialize: ->
      do @reset

    reset: ->
      do @refreshAttributes

    refreshAttributes: ->
      for attr in [ 'robot', 'scenario', 'algorithm' ]
        @updateUniqAttribute attr
      for attr in [ 'duration', 'distance', 'rotation' ]
        @updateMedianAttribute attr

    updateUniqAttribute: ( attr )->
      uniqueValues = []
      @get( 'tests' ).forEach ( model )->
        value = model.get attr
        uniqueValues.push value if value? and value not in uniqueValues

      @set attr + 's', uniqueValues
      switch uniqueValues.length
        when 0 then @set attr, 'None'
        when 1 then @set attr, uniqueValues[ 0 ]
        else @set attr, 'various'

    updateMedianAttribute: ( attr )->
      sum = num = 0
      @get( 'tests' ).forEach ( model )->
        value = +model.get( attr )
        if !isNaN( value )
          num++
          sum += value
      @set( attr, if num > 0 then sum/num else 'N/A' )
  

    getDataPointsForKey: ( key )->
      return @get( 'tests' ).map ( model )->
        return model.get key
