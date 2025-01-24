# Stage 1 - Python setup for both Django and bot
FROM python:3.11 AS base

# Set the working directory to /app
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

# Copy the current directory contents into the container
COPY . /app/

# Set environment variables for production
ENV PYTHONUNBUFFERED 1


# Stage 2 - Build Nginx for static files serving
FROM nginx:latest AS nginx

# Copy Nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Copy static files from the Django app
COPY --from=base /app/static /app/static

# Expose Nginx port
EXPOSE 80
EXPOSE 443

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
