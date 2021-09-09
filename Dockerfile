FROM python:3

WORKDIR /app

COPY . /app
COPY app/. /app
RUN pip install -r requirements.txt

EXPOSE 80

CMD [ "python", "main.py" ]