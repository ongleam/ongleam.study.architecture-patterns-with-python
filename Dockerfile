FROM python:3.11-slim-bookworm

RUN pip install flask "sqlalchemy>=1.4.0,<2.0.0" psycopg2-binary

RUN mkdir -p /code
COPY *.py /code/
COPY domain /code/domain
COPY adapters /code/adapters
COPY service_layer /code/service_layer
COPY entrypoints /code/entrypoints
WORKDIR /code
ENV FLASK_APP=entrypoints/flask_app.py FLASK_DEBUG=1 PYTHONUNBUFFERED=1
CMD flask run --host=0.0.0.0 --port=80
