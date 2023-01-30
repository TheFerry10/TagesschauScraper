FROM python:3.9-slim-buster

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python-dev \
        gcc \
        musl-dev \
        make \
        git \
        openssh-client \
        mypy \
        pandoc \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies:
COPY requirements.txt .

# Copy the application code into the container
COPY . .
CMD [ "/bin/bash" ]
