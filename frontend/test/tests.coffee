Backbone = require 'backbone'
testRequirejs.setupMocks
  'models/test': Backbone.Model

testRequirejs [ 'collections/tests' ], ( Tests )->
  describe 'Tests', ->
    it 'creates correctly', ->
      raw = [{ a:1 },{ b:2 },{ c: 3}]
      results = new Tests raw
      expect( results.toJSON() ).to.have.length 3
      expect( results.toJSON() ).to.eql raw

    describe 'groupBy', ->
      raw = [{ a: '1', b: '1' }, { a: '1', b: '2' }, { c: '3' }]

      it 'returns tasks grouped by one key', ->
        results = new Tests raw
        grouped = results.groupBy [ 'a' ]

        expect( grouped ).to.have.length 2
        for group in grouped
          expect( group ).to.be.instanceof Tests

        expect( grouped[ 0 ].toJSON() ).to.have.length 2
        expect( grouped[ 0 ].toJSON() ).to.eql [{ a: '1', b: '1' }, { a: '1', b: '2' }]
        expect( grouped[ 1 ].toJSON() ).to.have.length 1
        expect( grouped[ 1 ].toJSON() ).to.eql [{ c: '3' }]

      it 'returns tasks grouped by two keys', ->
        results = new Tests raw
        grouped = results.groupBy [ 'a', 'b' ]
        expect( grouped ).to.have.length 3
        for group in grouped
          expect( group ).to.be.instanceof Tests
          expect( group.toJSON() ).to.have.length 1

      it 'returns tasks grouped by three keys', ->
        results = new Tests raw
        grouped = results.groupBy [ 'a', 'b', 'c' ]
        expect( grouped ).to.have.length 3
        for group in grouped
          expect( group ).to.be.instanceof Tests
          expect( group.toJSON() ).to.have.length 1
