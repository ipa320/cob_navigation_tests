Backbone = require 'backbone'
MockTests = Backbone.Collection.extend {}
testRequirejs.setupMocks
  'collections/tests': MockTests

testRequirejs [ 'models/testGroup' ], ( TestGroup )->
  describe 'TestGroup', ->
    describe 'Constructor', ->
      checkDefaults = ( group )->
        #for attr in [ 'robot', 'algorithm', 'scenario' ]
          #expect( group.get attr ).to.equal 'None'
          #expect( group.get attr + 's' ).to.eql []
        #for attr in [ 'duration', 'distance', 'rotation' ]
          #expect( group.get attr ).to.equal 'N/A'

      it 'can handle empty args', ->
        group = new TestGroup
        expect( group ).to.be.instanceof TestGroup
        checkDefaults group

      it 'can handle non-empty args with undefined tests', ->
        group = new TestGroup id: 2
        expect( group ).to.be.instanceof TestGroup
        checkDefaults group

      it 'sets a new Tests Collection if args.tests is not an instanceof Tests', ->
        group = new TestGroup tests: [{ a: 1 }]
        expect( group.get 'tests' ).to.be.instanceof Backbone.Collection
        expect( group.get 'tests' ).to.have.length 1
        expect( group.get( 'tests' ).toJSON() ).to.eql [ a: 1 ]
        checkDefaults group

      it 'can handle an tests instance passed as args', ->
        tests = new MockTests { a: 1 }
        group = new TestGroup tests
        expect( group.has 'tests').to.be.true
        expect( group.get 'tests' ).to.be.instanceof Backbone.Collection
        expect( group.get 'tests' ).to.have.length 1
        expect( group.get( 'tests' ).toJSON() ).to.eql [ a: 1 ]
        checkDefaults group

      it 'uses the args.tests if it\'s an instanceof Tests (not cloned)', ->
        tests = new MockTests [{ a: 1 }]
        group = new TestGroup tests: tests
        expect( group.get 'tests' ).to.equal tests
        expect( group.get 'tests' ).to.have.length 1
        expect( group.get( 'tests' ).toJSON() ).to.eql [ a: 1 ]
        checkDefaults group

    describe 'Initialize', ->
      it 'sets a unique id', ->
        group1 = new TestGroup
        group2 = new TestGroup
        expect( group1 ).to.have.property 'id'
        expect( group1.get 'id' ).to.equal group1.id
        expect( group1.id ).to.be.a 'string'
        expect( group1.id ).to.have.length.above 0
        expect( group2.id ).to.not.equal( group1.id )

      it 'doesn\'t override given ids', ->
        group = new TestGroup id: 3
        expect( group.id ).to.equal 3

    describe 'Attributes', ->
      it 'sets None, #value, various to robot, scenario and algorithm', ->
        result = new TestGroup tests: [
          { robot: 'a', scenario: 'test' },
          { robot: 'b', scenario: 'test' }]

        expect( result.get 'robot' ).to.equal 'various'
        expect( result.get 'robots' ).to.eql [ 'a', 'b' ]

        expect( result.get 'scenario' ).to.equal 'test'
        expect( result.get 'scenarios' ).to.eql [ 'test' ]

        expect( result.get 'algorithm' ).to.equal 'None'
        expect( result.get 'algorithms' ).to.eql []


      it 'sets median value to duration, distance, rotation', ->
        result = new TestGroup tests: [
          { duration: 1, distance: 2, rotation: 3 },
          { duration: 4, distance: 5, rotation: 6 }]

        expect( result.get 'duration' ).to.equal 2.5
        expect( result.get 'distance' ).to.equal 3.5
        expect( result.get 'rotation' ).to.equal 4.5

    it 'getDataPointsForKeys returns test data', ->
      testsRaw = [
        { duration: 1, distance: 2, rotation: 3 },
        { duration: 4, distance: 5, rotation: 6 }]
      
      group = new TestGroup tests: testsRaw
      expect( group.getDataPointsForKey 'duration' ).to.eql [ 1, 4 ]
      expect( group.getDataPointsForKey 'distance' ).to.eql [ 2, 5 ]
      expect( group.getDataPointsForKey 'rotation' ).to.eql [ 3, 6 ]
