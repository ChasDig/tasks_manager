FROM python:3.13-slim

WORKDIR /tests/functional

ENV PYTHONPATH=/tests/functional

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . .
