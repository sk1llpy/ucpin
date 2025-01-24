# Stage 1 - Python setup
FROM python:3.11 AS base

# Set the working directory to /app
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container
COPY . /app/

# Expose the port that Gunicorn will use
EXPOSE 8000

# Set environment variables for production
ENV PYTHONUNBUFFERED 1


# Stage 2 - Nginx setup
FROM nginx:latest

# Copy the Nginx configuration file
COPY nginx.conf /etc/nginx/nginx.conf

# Copy static files from the Python stage
COPY --from=base /app/static /app/static

# Expose Nginx port
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
