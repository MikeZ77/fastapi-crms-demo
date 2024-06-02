FROM python:3.10-alpine

RUN apk add --no-cache --virtual .build-deps gcc postgresql-dev musl-dev python3-dev
RUN apk add libpq

RUN curl -sSL https://install.python-poetry.org | python3 -
    
WORKDIR /src
COPY . .
RUN poetry install --no-dev

CMD make run