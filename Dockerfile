FROM python:3.10-slim-buster

WORKDIR /app

RUN apt-get -qq update --fix-missing && apt-get -qq upgrade -y && apt-get install git -y

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 8181

CMD ["bash","start.sh"]
