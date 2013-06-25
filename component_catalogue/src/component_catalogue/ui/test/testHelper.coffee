global.expect = require( 'chai' ).expect
require( 'coffee-script' )
global.testRequirejs = require( './testRequirejs.coffee' )
global.testRequirejs.config({
  baseUrl: '../src',
  passthroughs: [ 'backbone', 'underscore' ]
});
