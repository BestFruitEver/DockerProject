FROM python:3

WORKDIR /app

COPY requirements.txt /app

RUN pip install -r requirements.txt
RUN apt-get install -y netcat

COPY . /app/

EXPOSE 8000
ENTRYPOINT ["bash","entrypoint.sh"]