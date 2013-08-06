#!/usr/bin/env python
import yaml, os, os.path
def relativeToAbsolutePath( suffix ):
    dirname = os.path.dirname( os.path.abspath( __file__ ))
    absPath = dirname + '/' + suffix
    return absPath

def getStreamForSrcFile( basename ):
    absPath = relativeToAbsolutePath( basename )
    stream  = file( absPath, 'r' )
    return stream

class ConfigObj( object ):
    def __init__( self, robot, navigation, route ):
        self.robot      = robot
        self.navigation = navigation
        self.route      = route

    def __str__( self ):
        format = 'Robot: %s, Navigation: %s, Route: %s'
        return format % ( self.robot, self.navigation, self.route )

def permutations():
    configStream = getStreamForSrcFile( 'config.yaml' )
    config       = yaml.load( configStream )
    for robot in config[ 'robots' ]:
        for navigation in config[ 'navigations' ]:
            for route in config[ 'routes' ]:
                yield ConfigObj( robot, navigation, route )

def generateLaunchfile( config ):
    templateStream = getStreamForSrcFile( 'template.launch' )
    with templateStream as f:
        launchfileCode = f.read()

    scenarioName = config.route
    filename = scenarioName + '.launch'
    launchfileCode = launchfileCode.replace( '$route$',      config.route )
    launchfileCode = launchfileCode.replace( '$robot$',      config.robot )
    launchfileCode = launchfileCode.replace( '$navigation$', config.navigation)
    launchfileCode = launchfileCode.replace( '$scenarioName$', scenarioName )
    return filename, launchfileCode

def updateCMakeListsTxt( paths ):
    cmakeAbsPath = relativeToAbsolutePath( '../../CMakeLists.txt' )
    with file( cmakeAbsPath, 'r' ) as f:
        cmakeContent = f.read()

    splitCode = '### GENERATED ###'
    cmakeContent = cmakeContent.split( splitCode )[ 0 ]

    cmakeContent += splitCode + "\n\n"
    rostestFormat = 'rosbuild_add_rostest(%s  TIMEOUT 10000.0)\n'
    for path in paths:
        cmakeContent += rostestFormat % path

    with file( cmakeAbsPath, 'w' ) as f:
        f.write( cmakeContent )

if __name__ == '__main__':
    cmakePaths = []
    for config in permutations():
        filename, launchfileCode = generateLaunchfile( config )
        cmakePath = 'launch/generated/' + filename
        cmakePaths.append( cmakePath )

        absPath = relativeToAbsolutePath( '../../' + cmakePath )
        with file( absPath, 'w' ) as f:
            f.write( launchfileCode )

    updateCMakeListsTxt( cmakePaths )



