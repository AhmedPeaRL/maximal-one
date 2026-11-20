FROM --platform=linux/amd64 python:3.11.15-slim@sha256:78b39ef14d8e2b4d71f8dc304f1328c37df95fe0ef99477c2ae6bd3d03784553

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
