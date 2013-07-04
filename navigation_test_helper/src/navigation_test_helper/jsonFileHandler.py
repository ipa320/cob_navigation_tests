import json, os.path

class JsonFileHandler( object ):
    def __init__( self, filename ):
        self._filename = filename
        self._values = {}

    def write( self, data ):
        content = [ data ]
        with open( self._filename, 'w' ) as f:
            f.write( json.dumps( content ))

    def append( self, data ):
        content = self.read()
        content.append( data )
        with open( self._filename, 'w' ) as f:
            f.write( json.dumps( content ))

    def read( self ):
        if os.path.isfile( self._filename ):
            with open( self._filename, 'r' ) as f:
                return json.loads( f.read() )
        return []
