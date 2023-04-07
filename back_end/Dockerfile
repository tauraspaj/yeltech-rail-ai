FROM python:3.10

RUN apt-get update
RUN apt-get install -y ffmpeg libsm6 libxext6 cron nano

WORKDIR /back_end

COPY back_end/requirements.txt .
RUN pip install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt

ENV PYTHONPATH "${PYTHONPATH}:/back_end/"

COPY back_end .

RUN mkdir /back_end/logs

COPY .env /back_end/.env
RUN chmod +x /back_end/.env

COPY common /back_end/common
COPY inferences /back_end/inferences
COPY assets /back_end/assets

COPY cron_jobs /etc/cron.d/cron_jobs
RUN chmod 0644 /etc/cron.d/cron_jobs
RUN crontab /etc/cron.d/cron_jobs
RUN touch /var/log/cron.log

EXPOSE 8296

COPY start.sh /back_end/start.sh
RUN chmod +x /back_end/start.sh

ENTRYPOINT ["/back_end/start.sh"]
