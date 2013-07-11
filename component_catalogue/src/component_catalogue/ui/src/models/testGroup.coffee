define [ 'backbone', 'underscore', 'collections/tests' ], ( Backbone, _, Tests )->
  TestGroup = Backbone.Model.extend
    defaults:
      selected:          undefined
      count:             0
      empty:             false
      robot:             'None'
      robots:            [],
      scenario:          'None'
      scenarios:         [],
      navigation:        'None'
      navigations:       []
      enabled:           true
      'mean.duration':   'N/A'
      'mean.distance':   'N/A'
      'mean.rotation':   'N/A'
      'stdDev.duration': 'N/A'
      'stdDev.distance': 'N/A'
      'stdDev.rotation': 'N/A'
      'mean.collisions': 'N/A'
      'std.collisions':  'N/A'
      indexesByCid:      {}
      errorsCombined:    0
      errorsAborted:     0
      errorsFailed:      0
      errorsMissed:      0
      errorsTimedout:    0

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
      @set 'originalTests',  @get 'tests'
      @set 'tests',          @get( 'tests' ).clone()
      @set 'indexesByCid',   @get( 'tests' ).getIndexesByCid()
      @once 'change:filters', ->
        do @setupFilters

    setupFilters: ()->
      for filter in @get 'filters'
        @listenTo filter, 'change', @filterChanged

    filterChanged: ->
      do @updateTestsLists
      do @refreshAttributes

    updateTestsLists: ->
      @applyFilters @get 'filters'

    filter: ( filter )->
      clone   = do @clone
      filters = clone.get( 'filters' ).concat filter
      clone.applyFilters filters
      clone

    applyFilters: ( filters )->
      newTests = @get( 'originalTests' ).filter filters
      @set 'tests', newTests


    reset: ->
      do @refreshAttributes

    refreshAttributes: ->
      for attr in [ 'robot', 'scenario', 'navigation' ]
        @updateUniqAttribute attr
      for attr in [ 'duration', 'distance', 'rotation', 'collisions' ]
        @updateMedianAttribute attr
        @updateStdDevAttribute attr
      do @updateErrorCount

      count = @get( 'tests' ).length
      @set 'count', count
      @set 'empty', count == 0

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
        return if model.get( 'error' )
        value = +model.get( attr )
        if !isNaN( value )
          num++
          sum += value
      @set( 'mean.' + attr, if num > 0 then sum/num else 'N/A' )
      
    updateErrorCount: ->
      errorsCombined = 0
      errorKeys     = [ 'Aborted', 'Failed', 'Missed', 'Timedout' ]
      errors        = {}
      errors[ key ] = 0 for key in errorKeys

      erroneous = @get( 'tests' ).forEach ( model )->
        return if not model.get 'error'
        errorsCombined++
        for key in errorKeys
          if key.lower() == model.get( 'error' ).lower()
            errors[ key ]++

      for key in errorKeys
        @set 'errors' + key, errors[ key ]


    updateStdDevAttribute: ( attr )->
      mean = @get 'mean.' + attr
      sum = num = 0
      @get( 'tests' ).map ( model )=>
        value = +model.get( attr )
        if !isNaN( value )
          num++
          sum += Math.pow ( value - mean ), 2
        @set 'stdDev.' + attr, if sum > 0 then Math.sqrt sum/num else 'N/A'

    getDataPointsForKey: ( key )->
      return @get( 'tests' ).map ( model )->
        return 'error' if model.get 'error'
        return model.get key

    getDetailedDataPointsForKey: ( key )->
      indexesByCid = @get 'indexesByCid'
      return @get( 'tests' ).map ( model )->
        date:  model.get 'date'
        error: model.get 'error'
        index: indexesByCid[ model.cid ]
        y:     model.get key

    groupBy: ->
      tests = @get 'tests'
      return tests.groupBy.apply tests, arguments

    sortBy: ->
      clone = do @clone
      tests = clone.get 'tests'
      sortedTests = tests.sortBy.apply tests, arguments
      clone.set 'tests', sortedTests, silent: true
      clone
