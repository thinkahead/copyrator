FROM docker.io/library/python:3.8.2-alpine
#FROM python:3.7.3-alpine3.9
#RUN apk add curl
ADD copyrator /app/copyrator
ADD setup.py /app/setup.py
RUN python -m pip install --upgrade pip
RUN pip3 install /app
COPY cert /cert
COPY cacert /cacert
COPY key /key
#RUN ls /usr/local/lib/python3.8/site-packages/kubernetes/config/
COPY incluster_config.py /usr/local/lib/python3.8/site-packages/kubernetes/config/incluster_config.py
#RUN find /usr/local/lib/ -name incluster_config.py
#RUN cat /usr/local/lib/python3.7/site-packages/copyrator/operator.py | grep labels
ENTRYPOINT ["copyrator"]
