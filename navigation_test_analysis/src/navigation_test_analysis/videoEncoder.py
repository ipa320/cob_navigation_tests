import subprocess

class RecorderSettings( object ):
    def __init__( self ):
        self.targetUri   = ''
        self.bagFilepath = ''
        self.display     = ':0'
        self.offset      = [ 0, 0 ]
        self.size        = [ 0, 0 ]
        self.frequency   = 0

    def sizeToString( self ):
        return '%s:%s' % tuple( self.size )

    def offsetToString( self ):
        return '%s,%s' % tuple( self.offset )


def assertInstalled():
    assertAvconvInstalled()
    assertCodecInstalled()

def assertAvconvInstalled():
    try:
        args   = 'avconv --help'.split( ' ' )
        p      = subprocess.Popen( args, stdout=subprocess.PIPE )
        result = p.wait()
    except OSError, e:
        raise Exception( 'Avconv is not installed on your system' )

def assertCodecInstalled():
    args = 'avconv -codecs'.split(  ' ' )
    p    = subprocess.Popen( args, stdout=subprocess.PIPE )
    stdout, stderr = p.communicate()
    if stdout.find( 'libx264' ) == -1:
        raise Exception( 'Codec libx264 not installed. You can try to install package "libavcodec-extra-53"' )

def recordToMkvFileCommand( mkvFile, settings ):
    return 'avconv -f x11grab -s %s -r %s -i %s+%s %s' % (
            settings.sizeToString(),
            settings.frequency,
            settings.display,
            settings.offsetToString(),
            mkvFile )

def encodeToMp4Command( mkvFile, mp4File ):
    return 'avconv -i %s -c:v libx264 %s' % ( mkvFile, mp4File )

if __name__ == '__main__':
    assertInstalled()
