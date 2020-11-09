FROM tiangolo/uwsgi-nginx-flask:latest
RUN apt-get update
ENV STATIC_URL /static
ENV STATIC_PATH app/static
COPY ./requirements.txt /var/www/requirements.txt
RUN pip install -r /var/www/requirements.txt

COPY . .
COPY /usr/share/nltk_data/tokenizers /usr/share/nltk_data/tokenizers
ENV LISTEN_PORT 5000

WORKDIR /app

EXPOSE 5000