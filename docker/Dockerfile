FROM ghcr.io/myoung34/github-runner:2.317.0
RUN apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir selenium && \
    apt-get clean && rm -rf /var/lib/apt/lists/*
