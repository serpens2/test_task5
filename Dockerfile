FROM python:3.11-slim
WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY quotes_of_the_day/ ./quotes_of_the_day/
EXPOSE 8000