from jsonFileHandler import JsonFileHandler

class ResultRepository( object ):
    def __init__( self, repository ):
        self._repository = repository

    def walkResults( self ):
        for dirname, filename in self._repository.walk():
            if not filename.startswith( 'result' ) or not filename.endswith( '.json' ):
                continue
            yield dirname, filename

    def allFilenamesAnalyzed( self ):
        allFilenamesAnalyzed = []
        for dirname, filename in self.walkResults():
            testResultHandler = JsonFileHandler( dirname + '/' + filename )
            nextFilename = map( lambda f: f[ 'filename' ], testResultHandler.read() )
            allFilenamesAnalyzed += nextFilename
        return allFilenamesAnalyzed

    def concated( self ):
        result = []
        for dirname, filename in self.walkResults():
            hdl = JsonFileHandler( dirname + '/' + filename )
            result += hdl.read()
        return result

