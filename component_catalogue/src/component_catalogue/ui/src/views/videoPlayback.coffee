define [ 'backbone', 'templates/videoPlayback' ], ( Backbone, videoPlaybackTmpl  )->
  Backbone.View.extend
    events:
      'click .close': 'hide'
    options:
      online: false

    render: ->
      html = do videoPlaybackTmpl
      @$el.html html
      @

    show: ->
      do @$el.show
      
    hide: ->
      do @$el.hide

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
