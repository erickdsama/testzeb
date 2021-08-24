FROM python:3.7

ADD . /flask
WORKDIR /flask
RUN pip install -r requirements.txt
RUN pip install gunicorn

RUN ["chmod", "a+x", "boot.sh"]

ENV FLASK_APP main.py

ENTRYPOINT ["./boot.sh"]
