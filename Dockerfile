# Stage 1: Dependency Installation
FROM python:3.11-slim AS builder

WORKDIR /app

RUN pip install --upgrade pip pip-tools

COPY requirements.in .

RUN pip-compile requirements.in -o requirements.txt

RUN pip install --no-cache-dir -r requirements.txt && pip check

# Stage 2: Runtime Image
FROM python:3.11-slim

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

COPY . .

ENV PYTHONUNBUFFERED=1
ARG AWS_REGION
ENV AWS_REGION=${AWS_REGION}

RUN useradd --create-home appuser
USER appuser

HEALTHCHECK --interval=30s --timeout=10s --retries=3 CMD python src/health_check.py || exit 1

CMD ["python", "-m", "src.main"]
