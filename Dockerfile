# Use an official Python runtime as a parent image
FROM python:3.11

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

# Stage 2 - Nginx Setup
FROM nginx:latest

COPY nginx.conf /etc/nginx/nginx.conf

COPY --from=base /app/static /app/static

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
