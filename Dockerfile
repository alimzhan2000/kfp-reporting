FROM python:3.9-slim

WORKDIR /app

COPY requirements-flask.txt .
RUN pip install -r requirements-flask.txt

COPY app.py .

EXPOSE 8000

CMD ["python", "app.py"]