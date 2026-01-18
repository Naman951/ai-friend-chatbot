FROM python:3.11-slim

WORKDIR /app

# Copy entire repo
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r backend/requirements.txt

# Set working directory to backend
WORKDIR /app/backend

# Expose port
EXPOSE 5000

# Run app
CMD ["python", "app.py"]


