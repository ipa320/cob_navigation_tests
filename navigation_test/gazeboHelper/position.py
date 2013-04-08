import math

class Position( object ):
    def __init__( self, x, y, theta ):
        self.x = x
        self.y = y
        self.theta = theta

    def __sub__( self, b ):
        # see http://stackoverflow.com/questions/1878907/
        #   the-smallest-difference-between-2-angles for diff alpha
        diffAlpha = ( self.theta - b.theta + math.pi ) % ( 2*math.pi ) - math.pi
        return Position( self.x - b.x, self.y - b.y, diffAlpha )

    def __eq__( self, b ):
        if not isinstance( b, Position ):
            return False
        return b.x == self.x and b.y == self.y and b.theta == self.theta

    def __ne__( self, b ):
        return not self == b

    def __str__( self ):
        return '{ x: %s, y: %s, theta: %s }' % ( self.x, self.y, self.theta )

    def abs( self ):
        return Position( math.fabs( self.x ), \
            math.fabs( self.y ), \
            math.fabs( self.theta ))
