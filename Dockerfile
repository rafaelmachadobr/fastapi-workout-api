FROM python:3.12.0-alpine

WORKDIR /home/python/app

RUN apk add --no-cache make

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["make", "run"]
