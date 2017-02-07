from __future__ import print_function
import boto3
import os
import sys
import pysftp
import logging
from base64 import b64decode

log = logging.getLogger()
log.setLevel( logging.INFO )

## SFTP CONFIG
knownhosts_file = open( '/tmp/knownhosts_file', 'w' )
knownhosts_file.write( boto3.client('kms').decrypt(CiphertextBlob=b64decode(os.environ['SFTP_KNOWNHOSTS_FILE']))['Plaintext'] )
knownhosts_file.close()
cnopts = pysftp.CnOpts( knownhosts='/tmp/knownhosts_file' )

sftp_config = {
    'host'     : os.environ['SFTP_HOST'],
    'username' : os.environ['SFTP_USERNAME'],
    'password' : boto3.client('kms').decrypt(CiphertextBlob=b64decode(os.environ['SFTP_PASSWORD']))['Plaintext'],
    'port'     : int( os.environ['SFTP_PORT'] ),
    'cnopts'   : cnopts
}

processLatestOnly = os.environ.get('PROCESS_LATEST_ONLY') or False

## S3 CONFIG
s3_bucket = os.environ['S3_BUCKET']

def sftp2S3( evt, cxt ):
    log.info( '-> Connecting onto the SFTP server' )
    sftp = pysftp.Connection( **sftp_config )
    log.info( '-> Successfully connected onto the SFTP server' )
    s3 = boto3.client( 's3' )
    log.info( '-> Instanciated S3 client' )

    if processLatestOnly:
        log.info( '-> Fetching latest file only' )
        latest_file = None
        for f in sftp.listdir_attr():
            log.debug( '-> Comparing %s' % f.filename )
            if latest_file is None or f.st_mtime > latest_file.st_mtime:
                log.debug( '-> %s is the most recent so far' % f.filename )
                latest_file = f
        if latest_file is not None:
            processFile( sftp, s3, latest_file )
    else:
        log.info( '-> Fetching all files' )
        for f in sftp.listdir_attr():
            processFile( sftp, s3, f )

    log.info( '-> All set ! exiting..' )
    sftp.close()

def processFile( sftp, f ):
    local_file = '/tmp/' + f.filename
    log.info( '--> Downloading %s from SFTP server' % f.filename )
    sftp.get( f.filename, local_file )
    log.info( '--> Uploading %s to S3 bucket (%s)' % ( f.filename, s3_bucket ) )
    s3.upload_file( local_file, s3_bucket, f.filename )
    log.info( '--> Cleaning up %s on SFTP server and locally' % f.filename )
    # os.remove( local_file )
    # sftp.remove( f.filename )
