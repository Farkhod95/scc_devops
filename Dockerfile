# Base image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt /app/

# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files
COPY . /app/

# Expose the required port
EXPOSE 8080

# Default command (overridden by docker-compose if needed)
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
CMD ["daphne", "-p", "8000", "main.asgi:application"]
