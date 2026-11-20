FROM --platform=linux/amd64 python:3.11.18-slim-trixie@sha256:b701198cb708b68d9413ca67d6311bd97c9389a2c5fe4da0511fc652642366cd

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

COPY requirements-lock.txt ./requirements-lock.txt
RUN python -m pip install \
      --no-cache-dir \
      --only-binary=:all: \
      --require-hashes \
      -r requirements-lock.txt \
    && python -m pip check

RUN groupadd --gid 10001 app \
    && useradd \
      --uid 10001 \
      --gid app \
      --create-home \
      --shell /usr/sbin/nologin \
      app

COPY --chown=10001:10001 . .

USER 10001:10001

ENTRYPOINT ["python", "-m", "scripts.generate_report"]
CMD ["--help"]
