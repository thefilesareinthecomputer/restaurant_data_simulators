# Base image
FROM python:3.11-slim

# Set environment variables to ensure output is logged
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /dash_app

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire dash_app directory into the container
COPY dash_app /dash_app

# Expose port 8050 (default for Dash apps)
EXPOSE 8050

# Command to run the Dash app
CMD ["python", "app.py"]
