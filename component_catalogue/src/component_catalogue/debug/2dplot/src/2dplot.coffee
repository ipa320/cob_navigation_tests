class Plot2D
  constructor: ( el )->
    $el      = $ el
    @width   = $el.width()
    @height  = $el.height()
    @paper   = Raphael $el[ 0 ], @width, @height
    @colors  = [ 'red', 'green' ]
    @padding = x: 10, y: 10

  drawCircleWithOrientationInRad: ( x, y, phi, color )->
    @drawCircleWithOrientationInDeg x, y, phi/2.0/Math.PI*360, color

  drawCircleWithOrientationInDeg: ( x, y, phi, color )->
    @drawArrow x, y, phi
    @drawCircle x, y, color

  drawCircle: ( x, y, color )->
    radius = 3.5
    circle = @paper.circle x, y+.5, radius
    circle.attr fill: color, stroke: 'transparent'

  drawStartPoint: ( points )->
    startPoint = points[ _.keys( points )[ 0 ]][ 0 ]
    nx = @normalizedX startPoint[ 1 ]
    ny = @normalizedY startPoint[ 2 ]
    c  = @paper.circle nx, ny, 10
    c.attr fill: 'orange', 'stroke-width': 0

  drawArrow: ( x, y, phi )->
    length = 15
    pathString = "M0,.5L#{length},.5"
    line = @paper.path pathString
    head = @drawArrowHead()
    line.transform "t#{x},#{y}r#{phi},0,.5"
    head.transform "t#{x+length},#{y}r#{phi},-#{length},.5"

  drawArrowHead: ->
    height = 4
    width  = 4
    y0 = -Math.floor( height/2 )-.5
    y1 = Math.ceil( height/2 )+1.5
    x1 = width+.5

    path = @paper.path "M.5,.5L.5,#{y0}L#{x1},.5L.5,#{y1}L.5,.5"
    path.attr 'fill', 'black'
    path

  adjustCanvasToPoints: ( points )->
    rawPoints = _( points ).chain().values().flatten( true ).value()
    x         = _.map rawPoints, ( p )->p[ 1 ]
    y         = _.map rawPoints, ( p )->p[ 2 ]

    [ xMin, xMax ] = [ _.min( x ), _.max( x ) ]
    @mx = ( @width - 2*@padding.x ) / ( xMax - xMin )
    @cx = @padding.x - @mx*xMin

    [ yMin, yMax ] = [ _.min( y ), _.max( y ) ]
    @my = ( @height - 2*@padding.y ) / ( yMax - yMin )
    @cy = @padding.y - @my*yMin

  normalizedX: ( x )->
    @mx*x+@cx

  normalizedY: ( y )->
    @my*y+@cy

  drawLine: ( linePoints, color )->
    linePath = [ 'M' ]
    for point in linePoints
      nx = Math.round( @normalizedX point[ 1 ]) + .5
      ny = Math.round( @normalizedY point[ 2 ]) + .5
      linePath.push nx, ',', ny, 'L'
    linePath.pop() # remove trailing L
    obj = @paper.path linePath.join ''
    obj.attr stroke: color

  plotPoints: ( points )->
    @paper.clear()
    @adjustCanvasToPoints points
    @drawStartPoint points
    i = 0
    for key, data of points
      color = @colors[ i++ ]
      @drawLine data, color

      for point in data
        [ x, y, phi ] = point[ 1..3 ]
        [ nx, ny ] = [ @normalizedX( x ), @normalizedY( y )]
        @drawCircleWithOrientationInRad nx, ny, phi, color

element = $ '#plot'
plot = new Plot2D element
plot.plotPoints points
