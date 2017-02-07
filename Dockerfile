FROM amazonlinux:latest

RUN \
curl -s https://bootstrap.pypa.io/get-pip.py | python ;\
yum install -y gcc zip python27-devel libffi-devel openssl-devel ;\
mkdir /release ;\
pip install pysftp -t /release

ADD sftp2S3.py /release/
