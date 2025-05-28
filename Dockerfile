FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN apt update && apt install -y lsof && pip install -r requirements.txt

CMD ["python", "app.py"]
