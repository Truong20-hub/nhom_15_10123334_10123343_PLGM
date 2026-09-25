# Dockerfile cho AI Service (Cổng 8001)
FROM python:3.12-slim

# Thiết lập biến môi trường
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8001

WORKDIR /app

# Cài đặt curl để hỗ trợ docker healthcheck
RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

# Cài đặt thư viện Python từ requirements.txt
COPY ai-models/requirements.txt .
RUN pip install --default-timeout=100 --retries 5 --no-cache-dir -r requirements.txt

# Sao chép model, schema, metadata và mã nguồn service
COPY ai-models/models/ ./models/
COPY ai-models/service/service.py .

# Thiết lập đường dẫn môi trường cho model
ENV MODEL_PATH=/app/models/model.joblib \
    SCHEMA_PATH=/app/models/schema.json \
    METADATA_PATH=/app/models/metadata.json

EXPOSE 8001

HEALTHCHECK --interval=15s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8001/health || exit 1

CMD ["uvicorn", "service:app", "--host", "0.0.0.0", "--port", "8001"]
