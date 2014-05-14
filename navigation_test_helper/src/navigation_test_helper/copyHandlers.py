import re, os, shutil, subprocess, commands

def getByUri( uri ):
    if SSHCopyHandler.matches( uri ):
        return SSHCopyHandler( uri )
    else:
        return LocalCopyHandler( uri )

class CopyException( Exception ):
    def __init__( self, source, target, err='' ):
        msg = 'Could not copy file %s to %s' % ( source, target )
        if err: msg += 'Err:\n%s' % err
        Exception.__init__( self, msg )

class SSHCopyHandler():
    pattern = '([^@]+)@([^:]+):(.+)'

    @staticmethod
    def matcher( uri ):
        return re.match( SSHCopyHandler.pattern, uri ) 

    @staticmethod
    def matches( uri ):
        return SSHCopyHandler.matcher( uri ) != None

    def __init__( self, uri ):
        matcher       = SSHCopyHandler.matcher( uri )
        self.username = matcher.group( 1 )
        self.host     = matcher.group( 2 )
        self.path     = matcher.group( 3 )

    def _sshOptions( self ):
        return ' '.join([
                '-o ConnectTimeout=30s',
                '-o PasswordAuthentication=no',
                '-o StrictHostKeyChecking=no' ])

    def _wrapBySsh( self, cmd ):
        ssh = 'ssh %s %s@%s' % ( self._sshOptions(), self.username, self.host )
        sshArgs = ssh.split( ' ' )
        cmdArgs = cmd.split( ' ' )
        return sshArgs + cmdArgs

    def assertWritable( self ):
        args = self._wrapBySsh( 'touch %s/.connection_test' % self.path )
        success, stdout = self._execute( args )
        if not success:
            msg  = "Couldn't write to directory %s as %s on host %s," % ( \
                    self.path, self.username, self.host )
            msg += "\n\ncmd: %s" % args
            msg += "\n\nstdout+sterr: %s" % stdout
            raise Exception( msg )
        return True

    def copyFile( self, localFilepath ):
        args = self._scpCommandArgs( localFilepath )
        success, stdout = self._execute( args )
        if not success:
            target = "%s@%s:%s/" % ( self.username, self.host, self.path )
            raise CopyException( localFilepath, target )

    def _scpCommandArgs( self, localFilepath ):
        filename = os.path.basename( localFilepath )
        cmd = 'scp %s %s %s@%s:%s/%s' % ( self._sshOptions(), localFilepath,
                self.username, self.host, self.path, filename )
        return cmd.split( ' ' )

    def _execute( self, args ):
        PIPE = subprocess.PIPE
        p    = subprocess.Popen( args, stdout=PIPE, stderr=PIPE )
        stdin, stdout = p.communicate()
        success       = p.returncode == 0
        return success, stdout


class LocalCopyHandler():
    def __init__( self, path ):
        self.path = os.path.expanduser( path )

    def assertWritable( self ):
        if not os.access( self.path, os.W_OK ):
            raise Exception( 'Cannot write to local file system on %s' %
                self.path )
        return True

    def copyFile( self, localFilepath ):
        filename       = os.path.basename( localFilepath )
        targetFilepath = '%s/%s' % ( self.path, filename )
        if localFilepath == targetFilepath:
            return True

        try:
            shutil.copyfile( localFilepath, targetFilepath )
        except IOError,e:
            raise CopyException( localFilepath, targetFilepath )
