FROM python:3.8 AS compile-image

RUN apt-get update

WORKDIR /app/

# не должно быть poetry.lock и .venv
COPY . /app/

RUN pip install "poetry"
RUN poetry config virtualenvs.in-project true && \
    poetry config virtualenvs.create true && \
    poetry install --no-interaction --no-ansi && \
    chmod -R +x /app/docker-entrypoint.sh

ENTRYPOINT ["/app/docker-entrypoint.sh"]
CMD ["server"]
CMD ["worker_1"]
CMD ["worker_2"]
