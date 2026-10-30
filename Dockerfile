# =====================================================================
# MedBot — Multi-Agent Medical Assistant Dockerfile
# Optimized for FastAPI backend (8000) and Streamlit UI (8501)
# =====================================================================

# 1. Minimal Python base image
FROM python:3.11-slim

# 2. Optimize Python runtime environment
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

WORKDIR /app

# 3. Install curl for container healthcheck
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

# 4. Copy & install dependencies first (layer caching)
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 5. Copy application source code
COPY app/ /app/app/
COPY streamlit_app.py /app/streamlit_app.py

# 6. Expose FastAPI (8000) and Streamlit (8501) ports
EXPOSE 8000 8501

# 7. Health check endpoint
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://127.0.0.1:8000/health || exit 1

# 8. Default command: Start FastAPI server
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

