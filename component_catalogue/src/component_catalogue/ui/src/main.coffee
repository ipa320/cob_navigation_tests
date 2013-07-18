require.config
  urlArgs: 'v=' + ( new Date() ).getTime()
  baseUrl: 'lib'
  shim:
    'backbone':
      deps: [ 'underscore', 'jquery' ],
      exports: 'Backbone'
    'underscore':
      exports: '_'
    'jquery':
      exports: '$'
    'jquery.dataTables':
      deps: [ 'jquery' ],
      exports: 'jQuery.fn.dataTable'
    'highcharts':
      deps: [ 'jquery' ],
      exports: 'jQuery.fn.highcharts'
    'highcharts-more':
      deps: [ 'highcharts' ],
      exports: 'jQuery.fn.highcharts'
    'jquery-ui':
      deps: [ 'jquery' ],
      exports: 'jQuery.fn'
    'jquery-numeric':
      deps: [ 'jquery' ],
      exports: 'jQuery.fn'
    'jquery-tipTip':
      deps: [ 'jquery' ],
      exports: 'jQuery.tipTip'
    'jquery.dataTables':
      deps: [ 'jquery' ],
      exports: 'jQuery.fn'
  paths:
    'templates':         '../templates',
    'backbone':          '../vendor/backbone',
    'underscore':        '../vendor/underscore',
    'jquery':            '../vendor/jquery-1.9.1',
    'jquery.dataTables': '../vendor/jquery.dataTables.min',
    'highcharts':        '../vendor/highcharts',
    'highcharts-more':   '../vendor/highcharts-more',
    'chosen':            '../vendor/chosen.jquery',
    'jquery-ui':         '../vendor/jquery-ui-1.10.2.custom',
    'jquery-numeric':    '../vendor/numeric'
    'jquery-tipTip':     '../vendor/jquery.tipTip.minified'

define [ 'app', 'backbone' ], ( app, Backbone )->
  do Backbone.history.start
  $.ajax
    url: '/data'
    dataType: 'json'
    success: ( data )->
      $( '#loading' ).fadeOut( 700 )
      app( data )
    error: -> alert( 'Could not load data' )
