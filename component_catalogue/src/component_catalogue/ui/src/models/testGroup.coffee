define [ 'backbone', 'underscore', 'collections/tests' ], ( Backbone, _, Tests )->
  TestGroup = Backbone.Model.extend
    defaults:
      selected:          undefined
      selectedTest:      null
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
      title:             ''

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
      @listenTo @get( 'tests' ), 'change:active', _.debounce @activeChanged, 100
      @set 'tests',         @get( 'tests' )
      @set 'indexesByCid',  @get( 'tests' ).getIndexesByCid()
      do @setupFilters if @get 'filters'

    setupFilters: ()->
      for filter in @get 'filters'
        @listenTo filter, 'change', @filterChanged

    activeChanged: ->
      do @refreshAttributes

    filterChanged: ->
      filters = @get 'filters'
      @get( 'tests' ).applyFilters filters

    reset: ->
      do @refreshAttributes

    refreshAttributes: ->
      for attr in [ 'robot', 'scenario', 'navigation' ]
        @updateUniqAttribute attr
      for attr in [ 'duration', 'distance', 'rotation', 'collisions' ]
        @updateMedianAttribute attr
        @updateStdDevAttribute attr
      do @updateErrorCount

      do @updateCount
      do @updateTitle

    updateTitle: ->
      @set 'title', [
        @get( 'robot' )
        '/'
        @get( 'navigation' )
        '/'
        @get( 'scenario' )
      ].join ' '

    updateCount: ( attr )->
      activeTests = @get( 'tests' ).filter ( test )->
        test.get 'active'
      @set 'count', activeTests.length
      @set 'empty',  @get( 'count' ) == 0

    updateUniqAttribute: ( attr )->
      uniqueValues = []
      @get( 'tests' ).forEach ( model )->
        return if not model.get 'active'
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
        return if not model.get 'active'
        return if model.get 'error'
        value = +model.get( attr )
        if !isNaN( value )
          num++
          sum += value
      @set 'mean.' + attr, if num > 0 then sum/num else 'N/A'
      
    updateErrorCount: ->
      errorsCombined = 0
      errorKeys     = [ 'Aborted', 'Failed', 'Missed', 'Timedout' ]
      errors        = {}
      errors[ key ] = 0 for key in errorKeys

      erroneous = @get( 'tests' ).forEach ( model )->
        return if not model.get 'error'
        errorsCombined++
        for key in errorKeys
          if key.toLowerCase() == model.get( 'error' ).toLowerCase()
            errors[ key ]++

      for key in errorKeys
        @set 'errors' + key, errors[ key ]
      @set 'errorsCombined', errorsCombined


    updateStdDevAttribute: ( attr )->
      mean = @get 'mean.' + attr
      sum = num = 0


      @get( 'tests' ).forEach ( model )=>
        return if not model.get 'active'
        return if model.get 'error'
        value = +model.get( attr )
        if !isNaN( value )
          num++
          sum += Math.pow ( value - mean ), 2
      #if @cid == 'c201'
      @set 'stdDev.' + attr, if sum > 0 then Math.sqrt sum/num else 'N/A'

    getDataPointsForKey: ( key )->
      return @get( 'tests' ).map ( model )->
        return 'error' if model.get 'error'
        return model.get key

    getDetailedDataPointsForKey: ( key )->
      indexesByCid  = @get 'indexesByCid'
      relevantTests = @get( 'test' )
      data          = []
      @get( 'tests' ).forEach ( model )->
        return if not model.get( 'active' )
        data.push
          date:  model.get 'date'
          error: model.get 'error'
          index: indexesByCid[ model.cid ]
          y:     model.get key
      data

    groupBy: ->
      tests = @get 'tests'
      return tests.groupBy.apply tests, arguments

    sortBy: ->
      clone = do @clone
      tests = clone.get 'tests'
      sortedTests = tests.sortBy.apply tests, arguments
      clone.set 'tests', sortedTests, silent: true
      clone
