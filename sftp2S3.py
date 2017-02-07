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

## S3 CONFIG
s3 = boto3.client( 's3' )
s3_bucket = os.environ['S3_BUCKET']

def sftp2S3( evt, cxt ):
    log.info( '-> Connecting onto the SFTP server' )
    sftp = pysftp.Connection( **sftp_config )
    log.info( '-> Successfully connected onto the SFTP server' )
    log.info( '-> Fetching files' )
    for f in sftp.listdir():
        local_file = '/tmp/' + f
        log.info( '--> Downloading %s from SFTP server' % f )
        sftp.get( f, local_file )
        log.info( '--> Uploading %s to S3 bucket (%s)' % ( f, s3_bucket ) )
        s3.upload_file( local_file, s3_bucket, f )
        log.info( '--> Cleaning up %s on SFTP server and locally' % f )
        os.remove( local_file )
        sftp.remove( f )
    log.info( '-> All set ! exiting..' )
    sftp.close()
