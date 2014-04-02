class Plot2D
  constructor: ( el )->
    $el    = $ el
    width  = $el.width()
    height = $el.height()
    @paper = Raphael $el[ 0 ], width, height

  drawCircleWithOrientation: ( x, y, phi, color )->
    @drawArrow x, y, phi
    @drawCircle x, y, color

  drawCircle: ( x, y, color )->
    radius = 3.5
    circle = @paper.circle x, y+.5, radius
    circle.attr 'fill', color
    circle.attr 'stroke', 'transparent'

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


element = $ '#plot'
plot = new Plot2D element
