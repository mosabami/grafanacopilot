FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install minimal build deps for asyncpg
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy and install backend requirements
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy repository into container
COPY . /app

EXPOSE 8000

# Start the app directly (runs python backend/src/app.py). This ensures the 'backend' package
# is importable because /app is on PYTHONPATH (working directory).
CMD ["python", "-u", "src/app.py"]
