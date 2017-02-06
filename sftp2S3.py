#!/usr/local/bin/python

from __future__ import print_function
import boto3
import os
import sys
import pysftp
import logging

log = logging.getLogger()
log.setLevel( logging.INFO )

## LOG TO CONSOLE (CAN BE REMOVED ON LAMBDA)
console = logging.StreamHandler( sys.stdout )
console.setLevel( logging.INFO )
console.setFormatter( logging.Formatter( '%(asctime)s - %(name)s - %(levelname)s - %(message)s' ) )
log.addHandler( console )

## SFTP CONFIG
cnopts = pysftp.CnOpts( knownhosts=os.environ['SFTP_KNOWNHOSTS_FILE'] )

sftp_config = {
    'host' :     os.environ['SFTP_HOST'],
    'username' : os.environ['SFTP_USERNAME'],
    'password' : os.environ['SFTP_PASSWORD'],
    'port' :     int( os.environ['SFTP_PORT'] ),
    'cnopts' :   cnopts
}

## S3 CONFIG
s3 = boto3.client( 's3' )
s3_bucket = os.environ['S3_BUCKET']

def sftp2S3():
    sftp = pysftp.Connection( **sftp_config )
    log.info( '-> Successfully connected onto the SFTP server' )
    log.info( '-> Fetching files' )
    for f in sftp.listdir():
        log.info( '--> Downloading %s from SFTP server' % f )
        sftp.get( f )
        log.info( '--> Uploading %s to S3 bucket (%s)' % ( f, s3_bucket ) )
        s3.upload_file( f, s3_bucket, f )
        log.info( '--> Cleaning up %s on SFTP server and locally' % f )
        os.remove( f )
        sftp.remove( f )
    log.info( '-> All set ! exiting..' )

sftp2S3()
