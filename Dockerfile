FROM python:3.10-alpine

RUN apk add --no-cache --virtual .build-deps gcc postgresql-dev musl-dev python3-dev
RUN apk add --no-cache make
RUN apk add libpq

EXPOSE 8000
EXPOSE 5679

RUN pip3 install poetry
    
WORKDIR /src
COPY . .
RUN poetry install

CMD poetry run fastapi run app/main.py --port 80 --reload