#!/usr/bin/env python
import os, json, math

def currentPath():
    return os.path.dirname( os.path.realpath( __file__ ))
def saveFile( filepath, content ):
    with open( filepath, 'w+' ) as f:
        f.write( content )

class Analyzer( object ):
    def __init__( self ):
        self._data = None

    def keys( self ):
        if not self._data or not len( self._data ):
            return []
        return self._data[ 0 ].keys()

    def loadData( self, filename ):
        if self._data is not None:
            return
        with open( filename, 'r' ) as f:
            lines = f.read().splitlines()
        jsonData = '[%s]' % ( ','.join( lines ))
        self._data = json.loads( jsonData )

    def getMean( self, key ):
        points = self.getPoints( key )
        return sum( points )/len( points )

    def getStandardDeviation( self, key ):
        mean = self.getMean( key )
        points = self.getPoints( key )
        deviations = []
        for point in points:
            var = ( point - mean )**2
            deviations.append( math.sqrt( var ))
        return deviations

    def getPoints( self, key ):
        return [ i[ key ]  for i in self._data ]

    def storeAnalyze( self, filepath ):
        result = {}
        for key in self.keys():
            result[ key ] = {
                'points': self.getPoints( key ),
                'mean':   self.getMean( key ),
                'stdDev': self.getStandardDeviation( key )
            }

        with file( filepath, 'w+' ) as f:
            f.write( json.dumps( result ))


class GnuPlot( object ):
    def __init__( self ):
        self._rows = []

    def addPoints( self, points ):
        self._rows.append( points )

    def addLine( self, lineValue ):
        self._rows.append([ lineValue ])

    def format( self ):
        data =  [ self._getTimeValues() ] + self._expandLines()
        return self._toDatFormat( data )

    def _expandLines( self ):
        data = self._rows[:]
        maxlen = self._getMaxLength()
        for i in xrange( 0, len( data )):
            item = data[ i ]
            if len( item ) == 1:
                data[ i ] = item*maxlen
        return data

    def _toDatFormat( self, data ):
        maxlen = self._getMaxLength()
        dat = ''
        for i in xrange( maxlen ):
            for row in data:
                if len( row ) <= i:
                    continue
                dat += '%s\t' % row[ i ]
            dat += '\n'
        return dat

    def _getTimeValues( self ):
        maxlen = self._getMaxLength()
        return range( maxlen )

    def _getMaxLength( self ):
        lens = ( len( i ) for i in self._rows )
        return max( lens )


analyzer = Analyzer()

analyzer.loadData( currentPath() + '/metrics.json' )
analyzer.storeAnalyze( currentPath() + '/analyzed.json' )

for key in analyzer.keys():
    gnuplot = GnuPlot()
    gnuplot.addPoints( analyzer.getPoints( key ))
    gnuplot.addLine( analyzer.getMean( key ))
    gnuplot.addPoints( analyzer.getStandardDeviation( key ))
    dat = gnuplot.format()
    saveFile( '%s/gnuplot/%s.dat' % ( currentPath(), key ), dat )
