FROM 104062/fz-bypass:latest

WORKDIR /app

COPY . .

CMD ["bash","start.sh"]
