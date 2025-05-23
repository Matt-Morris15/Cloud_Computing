FROM python:3.11

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["gunicorn", "-b", ":8080", "main:app"]
