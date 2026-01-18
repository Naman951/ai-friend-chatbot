FROM python:3.11-slim

WORKDIR /app

# Copy requirements
COPY backend/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ .

# Copy .env if exists (optional)
COPY backend/.env .env 2>/dev/null || true

# Expose port
EXPOSE 5000

# Run app
CMD ["python", "app.py"]
