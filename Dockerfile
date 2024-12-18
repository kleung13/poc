FROM python:3.12.8-alpine

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

ENV JWT_SECRET_KEY="poc"

EXPOSE 5000

CMD ["flask", "run", "--host", "0.0.0.0"]

