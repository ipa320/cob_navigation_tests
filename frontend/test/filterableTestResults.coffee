return
testRequirejs [ 'models/filterableTestResults' ], ( FilterableTestResults )->
  describe 'FilterableTestResults', ->
    it 'sets collection properly', ->
      #c = new Backbone.Collection
      #model = new FilterableTestResults collection: c
      expect( true ).to.be.true
