FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install minimal build deps for asyncpg
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory to /app/backend so that running `python src/app.py` inside
# the image computes REPO_ROOT as /app (two levels up from /app/backend/src/app.py).
WORKDIR /app/backend

# Copy and install backend requirements (cacheable layer)
COPY requirements.txt /app/backend/requirements.txt
RUN pip install --no-cache-dir -r /app/backend/requirements.txt

# Copy backend repository content into the image
COPY . /app/backend

EXPOSE 8000

# Start the app directly (runs python src/app.py). This mirrors the local
# command `python src/app.py` when run from the backend folder.
CMD ["python", "-u", "src/app.py"]
