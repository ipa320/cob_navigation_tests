Backbone = require 'backbone'
MockTestGroup = Backbone.Model.extend {}

testRequirejs.setupMocks
  'models/testGroup': MockTestGroup

testRequirejs [ 'collections/testGroups' ], ( TestGroups )->
