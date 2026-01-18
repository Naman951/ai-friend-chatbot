FROM python:3.11-slim

WORKDIR /app

# Copy entire repo
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r backend/requirements.txt

# Expose port
EXPOSE 5000

# Run app from backend folder
CMD ["python", "backend/app.py"]


