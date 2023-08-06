FROM python:3.8-slim AS venv

ARG project_dir
ARG venv_path

COPY ./ /tmp/

RUN set -x \
 && python3 -m venv ${venv_path} \
 && ${venv_path}/bin/pip install "/tmp[dev,doc,test]"


FROM python:3.8-slim

ARG venv_path

RUN set -x \
 && apt-get update \
 && apt-get install -y --no-install-recommends \
      git=1:2.30.2-1 \
 && rm -rf /var/lib/apt/lists/* \
 && git config --global user.email "you@example.com" \
 && git config --global user.name "Your Name"

COPY --from=venv ${venv_path} ${venv_path}
