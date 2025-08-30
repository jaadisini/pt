FROM python:latest

RUN pip3 install -U pip

WORKDIR /app
COPY . /app

RUN chown -R 1000:0 /app/
RUN chmod -R 777 /app/

RUN pip3 install -U -r requirements.txt

CMD ["bash", "start"]


