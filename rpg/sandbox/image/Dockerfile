FROM debian:12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
        bash \
        coreutils \
        procps \
        grep \
        findutils \
        sed \
        gawk \
    && rm -rf /var/lib/apt/lists/*

COPY seed/ /opt/seed/
RUN chmod +x /opt/seed/*.sh

CMD ["sleep", "infinity"]
