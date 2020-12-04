FROM python:3.7-buster

COPY requirements.txt /tmp/requirements.txt

RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && \
    unzip awscliv2.zip && ./aws/install && \
     rm -rf aws awscliv2.zip

RUN pip install -r /tmp/requirements.txt
