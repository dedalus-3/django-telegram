FROM python:3.8-slim-buster

# Не будет создавать pyc файлы.
ENV PYTHONDONTWRITEBYTECODE 1
# Гарантирует, что наш вывод консоли выглядит знакомым и не буферизируется Docker
ENV PYTHONUNBUFFERED 1

WORKDIR /home/dedalus

COPY requirements.txt ./requirements.txt
# install psycopg2 dependencies
#RUN apk update \
#    && apk add postgresql-dev gcc python3-dev musl-dev
RUN mkdir /home/dedalus/static && mkdir /home/dedalus/uploads

RUN apt-get update && apt-get install -y netcat \
    && pip install --upgrade pip \
    && pip install -r requirements.txt

# copy entrypoint.sh
# COPY entrypoint.sh ./entrypoint.sh

# copy project
COPY . .

# Run entrypoint.sh
ENTRYPOINT ["/home/dedalus/entrypoint.sh"]