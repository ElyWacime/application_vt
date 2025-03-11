FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    curl \
    wget \
    git \
    libpango-1.0-0 \
    libgdk-pixbuf-2.0-0 \
    libffi-dev \
    libcairo2 \
    libpangocairo-1.0-0 \
    unzip \
    curl \
    vim \
    tmux \
    nginx

WORKDIR /flask-app-pdf-v2

COPY flask-app-pdf-v2 .
COPY nginx.conf /etc/nginx/sites-available/
COPY .tmux.conf /root/.tmux.conf
COPY .tmux.conf .tmux.conf

RUN mv /etc/nginx/sites-available/nginx.conf /etc/nginx/sites-available/application_vt
RUN ln -s /etc/nginx/sites-available/file /etc/nginx/sites-enabled/application_vt

RUN curl -sSL https://ngrok-agent.s3.amazonaws.com/ngrok.asc \
    | tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null \
    && echo "deb https://ngrok-agent.s3.amazonaws.com buster main" \
    | tee /etc/apt/sources.list.d/ngrok.list \
    && apt update \
    && apt install ngrok

RUN python3 -m venv venv \
    && . venv/bin/activate \
    && pip install --upgrade pip \
    && pip install -r requirements.txt
s
RUN mkdir /var/www && \
    mkdir /var/www/vt_maps

COPY maps_index.html /var/www/vt_maps

EXPOSE 8080 80

CMD ["bash"]
