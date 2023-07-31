FROM python:3.10.6

ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
RUN echo "postfix postfix/main_mailer_type select Internet Site" | debconf-set-selections \
    && echo "postfix postfix/mailname string gorrasykmisetas.com" | debconf-set-selections

COPY . /app

RUN apt-get update && apt-get install -y postfix
RUN apt-get update && apt-get install -y cron
COPY postfix_main.cf /etc/postfix/main.cf
COPY sender_access /etc/postfix/sender_access
COPY generic /etc/postfix/generic
COPY cronjob /etc/cron.d/cronjob

RUN crontab /etc/cron.d/cronjob
RUN postmap /etc/postfix/sender_access && postmap /etc/postfix/generic
RUN pip install -r requirements.txt
EXPOSE 8002
ENV DJANGO_SETTINGS_MODULE=iati.settings

COPY run.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
CMD ["/entrypoint.sh"]