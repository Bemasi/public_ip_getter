FROM python:3.11-slim

WORKDIR /app
COPY email_replier.py .

RUN pip install requests

CMD ["python", "email_replier.py"]