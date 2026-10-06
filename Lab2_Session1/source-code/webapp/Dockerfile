# Dockerfile for the lab web app
FROM python:3.12-alpine
WORKDIR /app
COPY app.py .
ARG APP_VERSION=1.0
ARG APP_COLOR=#1f6feb
ENV APP_VERSION=$APP_VERSION \
    APP_COLOR=$APP_COLOR
EXPOSE 5000
USER nobody
CMD ["python", "app.py"]
