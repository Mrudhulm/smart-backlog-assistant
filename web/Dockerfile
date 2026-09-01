FROM python:3.11-slim

WORKDIR /app

# Keep timestamps consistent and make the container runtime self-describing.
ENV TZ=UTC \
    PYTHONUNBUFFERED=1

ARG DEFAULT_MODEL="gemini-3.6-flash"
ARG APP_USERNAME="mrudhul"

ENV DEFAULT_MODEL=${DEFAULT_MODEL} \
    APP_USERNAME=${APP_USERNAME}

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all core components including config, src, and web
COPY config/ ./config/
COPY src/ ./src/
COPY web/ ./web/

# Create necessary directories
RUN mkdir -p inputs outputs

# Create and switch to a non-root system user for security
RUN useradd -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 5000

CMD ["python", "web/app.py"]