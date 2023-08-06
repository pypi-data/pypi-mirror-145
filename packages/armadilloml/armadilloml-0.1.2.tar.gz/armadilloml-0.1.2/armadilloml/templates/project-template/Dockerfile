FROM python:3.9-slim-buster

RUN apt-get update && \
  apt-get upgrade -y && \
  apt-get install -y git

WORKDIR /
COPY ./ ./

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
RUN pip3 install poetry
RUN poetry install

EXPOSE 8080
EXPOSE ${port}

CMD exec poetry run gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app ./