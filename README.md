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

- `CLEAN_SFTP_FILES` : **OPTIONAL** *BOOLEAN* Cleanup files on SFTP (defaults to: False)
- `PROCESS_LATEST_ONLY` : **OPTIONAL** *BOOLEAN* Choose whether to process all files or the most recent one only (defaults to: False)
- `S3_BUCKET` : **MANDATORY** *STRING* This is the name of the destination bucket
- `SFTP_PORT` : **MANDATORY** *INTEGER* SFTP server TCP port
- `SFTP_HOST` : **MANDATORY** *STRING* SFTP server hostname
- `SFTP_USERNAME` : **MANDATORY** *STRING* SFTP server username
- `SFTP_PASSWORD` : **MANDATORY** *STRING* *ENCRYPTED* SFTP server password
- `SFTP_KNOWNHOSTS_FILE` : **MANDATORY** *STRING* *ENCRYPTED* SFTP server signature

### Find the SFTP server signature

```bash
ssh-keyscan  2>/dev/null
```
