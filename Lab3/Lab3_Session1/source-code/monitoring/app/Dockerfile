FROM python:3.12-alpine
RUN pip install --no-cache-dir prometheus_client==0.21.1
WORKDIR /app
COPY app.py .
EXPOSE 8000 8001
CMD ["python", "app.py"]
