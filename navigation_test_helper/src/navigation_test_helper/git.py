#!/usr/bin/env python
import sys, argparse, tempfile, subprocess, shutil, os, string, errno

class Git( object ):
    def __init__( self, repository, path=None ):
        self._repository = repository
        self._path = path or tempfile.mkdtemp( '_nav_git' )

    def __enter__( self ):
        p = subprocess.call([ 'git', 'clone', self._repository, self._path ])
        return Repository( self._path )

    def __exit__( self, type, value, traceback ):
        shutil.rmtree( self._path )

class Repository( object ):
    def __init__( self, path ):
        self._path = path

    def walk( self ):
        for root, dirnames, filenames in os.walk( self._path ):
            for filename in filenames:
                yield root, filename

    def mkdir( self, subdirectories ):
        subdirectories = [ self._sanitzePathname( d ) for d in subdirectories ]
        path = '%s/%s' % ( self._path, '/'.join( subdirectories ))
        self._mkdir_p( path )
        return path

    def commitAllChanges( self, msg ):
        p = subprocess.Popen([ 'git', 'add', '.' ], cwd=self._path )
        p.wait()
        p = subprocess.Popen([ 'git', 'commit', '-m', msg ], cwd=self._path )
        p.wait()

    def pullAndPush( self ):
        self.pull()
        self.push()

    def pull( self ):
        p = subprocess.Popen([ 'git', 'pull', 'origin', 'master' ], cwd=self._path )
        p.wait()

    def push( self ):
        p = subprocess.Popen([ 'git', 'push', 'origin', 'master' ], cwd=self._path )
        p.wait()


    def _sanitzePathname( self, path ):
        valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
        return ''.join( c for c in path if c in valid_chars )

    def _mkdir_p( self, path ):
        try:
            os.makedirs(path)
        except OSError as exc: # Python >2.5
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else: raise
