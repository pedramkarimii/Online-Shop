FROM python:latest

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN mkdir -p /app
WORKDIR /app
COPY . .

RUN pip install -U pip
RUN pip install -r requirements.txt --index-url=https://pypi.org/simple/
RUN pip install -r requirements.txt