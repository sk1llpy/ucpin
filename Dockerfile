# Use an official Python runtime as a parent image
FROM python:3.11

# Set the working directory to /app
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container
COPY . /app/

# Set environment variables for production
ENV PYTHONUNBUFFERED 1

# Expose the port Gunicorn will listen on
EXPOSE 8000

# Set the entrypoint for Gunicorn to serve the Django app
CMD ["gunicorn", "conf.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]