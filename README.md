# Lambda SFTP2S3

## Architecture

This AWS Lambda function fetches files from an SFTP server and copies them onto a
given S3 Bucket.

```
+-------------------+           +--------------------+          +--------------------+
|                   |           |                    |          |                    |
|       SFTP        <-----------+       LAMBDA       +---------->      S3 BUCKET     |
|                   +----------->                    |          |                    |
+-------------------+           +--------------------+          +--------------------+
```

## Build ZIP

```bash
docker build -t lambda-python-pysftp .
docker run -it --rm -v ~/:/output lambda-python-pysftp bash -c "cd /release; zip -r /output/sftp2S3.zip ."
```

## Configuration

### Environment variables

- `S3_BUCKET` : **MANDATORY** This is the name of the destination bucket
- `SFTP_PORT` : **MANDATORY** SFTP server TCP port
- `SFTP_HOST` : **MANDATORY** SFTP server hostname
- `SFTP_USERNAME` : **MANDATORY** SFTP server username
- `SFTP_PASSWORD` : **MANDATORY** *ENCRYPTED* SFTP server password
- `SFTP_KNOWNHOSTS_FILE` : **MANDATORY** _ENCRYPTED_ SFTP server signature
