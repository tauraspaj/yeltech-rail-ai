FROM python:3.10

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6 -y

WORKDIR /back_end

COPY back_end/requirements.txt .
RUN pip install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt

ENV PYTHONPATH "${PYTHONPATH}:/back_end/"

COPY back_end .

RUN mkdir /back_end/logs

COPY common /back_end/common
COPY inferences /back_end/inferences
COPY assets /back_end/assets

EXPOSE 8296

ENTRYPOINT ["gunicorn", "-c", "python:configs.gunicorn", "run:app"]
