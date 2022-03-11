#!/bin/sh

export PATH="/usr/local/bin/python/bin:$PATH"

apk add --update --no-cache --virtual .build-deps alpine-sdk python3-dev musl-dev libffi-dev libpq  postgresql-dev openssh-keygen \
&& pip install -U setuptools pip \
&& pip install poetry \
&& poetry config virtualenvs.create false \
&& poetry install --no-dev \
&& apk --purge del .build-deps \
&& gunicorn server:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000


#&& alembic upgrade head \