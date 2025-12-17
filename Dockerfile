FROM python:3.10.19-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends build-essential

COPY requirements.txt .

RUN pip install --user --no-cache-dir -r requirements.txt


FROM python:3.10.19-slim

WORKDIR /app

COPY --from=builder /root/.local /root/.local

COPY . .
#HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 CMD ["curl", "http://localhost:8000/api/v1/health"]

EXPOSE 8000

CMD [ "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000" ]


