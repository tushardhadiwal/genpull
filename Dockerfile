# // Copyright (c) Microsoft Corporation.
# // Licensed under the MIT license.
FROM python:3.7-slim

RUN  mkdir /opt/genpull

ENV VIRTUAL_ENV=/opt/genpull/genpull-env
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY ./requirements.txt /opt/genpull/requirements.txt
RUN pip install -r /opt/genpull/requirements.txt

WORKDIR /opt/genpull
COPY utils /opt/genpull/utils
COPY ./genpull.py /opt/genpull/genpull.py


CMD ["python", "/opt/genpull/genpull.py"]