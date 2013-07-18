define [ 'backbone' ], ( Backbone )->
  Backbone.View.extend
    options:
      online: false

    videoExists: ( filename )->
      dfd = @videosExist([ filename ])
      return dfd.pipe ( results )-> results[ 0 ]

    videosExist: ( filenames )->
      if !@options.online
        dfd = do $.Deferred
        dfd.reject 'Could not connect to the video server'
      else
        dfd = @query exists: filenames
      dfd
    
    query: ( data )->
      $.ajax
        url:         '/video'
        crossDomain: true
        data:        data
        dataType:    'jsonp'
