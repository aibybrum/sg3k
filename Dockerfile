FROM python:3.9 as requirements-stage

WORKDIR /tmp

RUN pip install poetry \
    && poetry self add poetry-plugin-export

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes --with notebook


FROM jupyter/minimal-notebook:latest

WORKDIR /home/jovyan

COPY --from=requirements-stage /tmp/requirements.txt /home/jovyan/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /home/jovyan/requirements.txt

EXPOSE 8888

CMD ["start-notebook.sh", "--NotebookApp.token="]