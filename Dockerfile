FROM python:3.11-slim

WORKDIR /dash_app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY dash_app/ /dash_app/

CMD ["python", "/dash_app/app.py"]
