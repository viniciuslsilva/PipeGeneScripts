
FROM python:3.6-slim-bullseye
WORKDIR /code

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install dependencies:
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 5011
# EXPOSE 5002
# EXPOSE 5001