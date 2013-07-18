define [ 'backbone', 'templates/videoPlayback', 'flowplayer' ], ( Backbone, videoPlaybackTmpl, flowplayer  )->
  Backbone.View.extend
    events:
      'click .close': 'hide'
    options:
      online: false

    render: ->
      html = do videoPlaybackTmpl
      @$el.html html
      @$el.hide()
      @

    play: ( src )->
      html = videoPlaybackTmpl src: src
      @$el.html html
      _.defer =>
        @$( '.flowplayer' ).flowplayer swf: "assets/flowplayer/flowplayer.swf"
        console.log 'play'
        do @show

    show: ->
      console.log 'show'
      do @$el.show
      
    hide: ->
      do @$el.hide
      @$el.html ''

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
