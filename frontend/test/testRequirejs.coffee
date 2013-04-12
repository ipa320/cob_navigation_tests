_ = require 'underscore'
path = require 'path'
configuration =
  paths: []
  mocks: {}
  passthroughs: []
  baseUrl: '.'

testRequirejs = ( testDependencies, testCallback ) ->
  testModules = []
  c = configuration
  defineCalled = false

  rewriteDepPath = ( dep )->
    for alias, dest of configuration.paths
      matcher = dep.match "^#{alias}(.*)"
      continue if not matcher
      dep = dest + matcher[ 1 ]
    dep


  global.define = ( moduleDependecies, moduleCallback ) ->
    defineCalled = true
    moduleArguments = []
    for dep in moduleDependecies
      dep = rewriteDepPath dep
      arg = c.mocks[ dep ] 
      if !arg && dep in c.passthroughs
        arg = require dep
      throw "No mock Object for dependency #{dep}" if !arg?
      moduleArguments.push arg
    module = moduleCallback.apply null, moduleArguments
    testModules.push module

  for dep in testDependencies
    err = null
    defineCalled = false
    try
      modulePath = configuration.baseUrl + '/' + dep
      module = require modulePath
      testModules.push module if not defineCalled
    catch error
      try
        module = require dep
        testModules.push module if not defineCalled
      catch error2
        throw "Cannot find module #{dep}:  #{error}"


  testCallback.apply null,testModules

testRequirejs.setupMocks = ( mocks )->
  _.extend configuration.mocks, mocks || {}

testRequirejs.config = ( config )->
  _.extend configuration, config

module.exports = testRequirejs
