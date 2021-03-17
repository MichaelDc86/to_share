#!/bin/bash

server() {

  export HOST=${HOST:-0.0.0.0}
  export PORT=${PORT:-8080}
  export APP_NAME=${APP_NAME:-sqrt}
  export WEB_WORKERS=${WEB_WORKERS:-1}

  exec gunicorn rest_app:app -b ${HOST}:${PORT} --name ${APP_NAME} -t 200 -w${WEB_WORKERS} -k uvicorn.workers.UvicornWorker --access-logfile - --error-logfile -
}

worker_1() {
  export HOSTNAME=${HOSTNAME:-0.0.0.0}
  echo "Starting worker..."

  export LOG_LEVEL=${LOG_LEVEL:-info}
  export APP_NAME=${APP_NAME:-sqrt}

  exec celery -A celery_app worker -l ${LOG_LEVEL} --concurrency=2 -E --hostname="${APP_NAME}.@${HOSTNAME}"
}

worker_2() {
  export HOSTNAME=${HOSTNAME:-0.0.0.1}
  echo "Starting worker..."

  export LOG_LEVEL=${LOG_LEVEL:-info}
  export APP_NAME=${APP_NAME:-sqrt}

  exec celery -A celery_app worker -l ${LOG_LEVEL} --concurrency=2 -E --hostname="${APP_NAME}.@${HOSTNAME}"
}
