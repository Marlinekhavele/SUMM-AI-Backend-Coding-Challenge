FROM python:3.9-slim

WORKDIR /translation

COPY requirements.txt /translation/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /translation/

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app.wsgi:application"]