FROM python:3.8-alpine3.12

RUN apk update \
   && apk add --no-cache build-base

ADD requirements.txt .
RUN pip install -r requirements.txt

ADD app.py /vk/
WORKDIR /vk/

CMD python3.8 app.py