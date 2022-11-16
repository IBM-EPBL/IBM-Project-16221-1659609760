FROM python:2-alpine

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r /app/requirements.txt

COPY . /app

ENTRYPOINT [ "python" ]

CMD [ "app.py" ]