import re, os

class BagInfo( object ):
    STATUS_NOT_ANALYZED = None
    STATUS_ANALYZED     = 'analyzed'
    STATUS_FIXED        = 'fixed'
    STATUS_ERROR        = 'error'

    @staticmethod
    def fileMatcher( uri ):
        return re.match( '(.*\.bag)(?:_([a-z]+))?$', uri )

    @staticmethod
    def isBagFile( uri ):
        fileIsBagFile = BagInfo.fileMatcher( uri ) != None
        fileFromRosbagReindex = uri.find( '.orig.bag' ) > -1 
        # ignore files created by rosbag reindex
        return fileIsBagFile and not fileFromRosbagReindex

    def __init__( self, filepath ):
        self._updateAttributes( filepath )

    def _updateAttributes( self, filepath ):
        self.filepath  = filepath
        self.filename  = os.path.basename( filepath )
        self.directory = os.path.dirname( filepath )
        self._fillRawFilenameAndStatus()

    def _fillRawFilenameAndStatus( self ):
        matcher = self.fileMatcher( self.filename )
        self.rawFilename = matcher.group( 1 )
        self.status      = matcher.group( 2 )

    def isProcessed( self ):
        return not self.isNotAnalyzed()


    def isNotAnalyzed( self ):
        return self.status == BagInfo.STATUS_NOT_ANALYZED or \
                self.status == BagInfo.STATUS_FIXED

    def isFixed( self ):
        return self.status == BagInfo.STATUS_FIXED

    def isErroneous( self ):
        return self.status == BagInfo.STATUS_ERROR

    def setAnalyzed( self ):
        self.setStatus( BagInfo.STATUS_ANALYZED )

    def setErroneous( self ):
        self.setStatus( BagInfo.STATUS_ERROR )

    def setFixed( self ):
        self.setStatus( BagInfo.STATUS_FIXED )

    def setStatus( self, status ):
        if self.isProcessed():
            raise Exception( 'File already has a status. Code: %s' % self.status )
        newFilepath = self._filepathForStatus( status )
        print 'src: %s, target: %s' % ( self.filepath, newFilepath )
        os.rename( str( self.filepath ), str( newFilepath ))
        self._updateAttributes( newFilepath )

    def _filepathForStatus( self, status ):
        if status:
            newFilename = "%s_%s" % ( self.rawFilename, status )
        else:
            newFilename = self.rawFilename
        newFilepath = "%s/%s" % ( self.directory, newFilename )
        return newFilepath
