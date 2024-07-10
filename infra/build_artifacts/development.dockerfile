#
# Layers: Only the instructions RUN, COPY, ADD create layers.
#

ARG PYTHON_IMAGE_VERSION=3.10

#
### Target: development
#
FROM python:${PYTHON_IMAGE_VERSION}-slim-buster as development

ENV USER_ID=1000
ENV GROUP_ID=1000

ENV USER=web
ENV HOME="/${USER}"

ENV \
    POETRY_VERSION=1.0.10 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    # write messages immediately to stream
    PYTHONUNBUFFERED=1 \
    # don't write .pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    # disable pip version check for speed reasons
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    # disable caching for installation and source files from pip
    PIP_NO_CACHE_DIR=1 \
    # virtual env path
    VENV_PATH="${HOME}/.venv"

ENV PATH="$HOME/.local/bin:$VENV_PATH/bin:$PATH"

ENV \
    # Do not use randomization for python seed
    PYTHONHASHSEED=1

# install pg_isready helper from postgres
RUN apt-get update \
    && apt-get install -y curl gnupg build-essential libpq-dev

RUN addgroup --gid ${GROUP_ID} ${USER}
RUN adduser --disabled-password --gecos '' --home "${HOME}" --uid "${USER_ID}" --gid "${GROUP_ID}" "${USER}"

USER ${USER}
WORKDIR ${HOME}

RUN pip install --user poetry

COPY --chown=${USER_ID}:${GROUP_ID} ./pyproject.toml ./poetry.lock ${HOME}/

RUN poetry install
RUN pip uninstall psycopg2-binary -y
RUN pip install psycopg2

COPY --chown=${USER_ID}:${GROUP_ID} ./app ${HOME}/app/
COPY --chown=${USER_ID}:${GROUP_ID} ./infra/build_artifacts/docker-entrypoint.sh ${HOME}/scripts/
COPY --chown=${USER_ID}:${GROUP_ID} ./alembic.ini ${HOME}/
COPY --chown=${USER_ID}:${GROUP_ID} ./tests ${HOME}/tests/

EXPOSE 8000

ENTRYPOINT ./scripts/docker-entrypoint.sh