# Python image to use.
FROM gcr.io/aashe-migration/hub-base-image:5163ad5b-1ede-4780-947e-7e4eb8d048f6

# Set the working directory to /app
WORKDIR /app

# Make directories for django and celery
RUN mkdir -p /var/www/ \
    mkdir -p /var/www/hub \
    mkdir -p /var/www/hub/media \
    mkdir -p /var/www/hub/static \
    mkdir -p /var/www/hub/logs \
    mkdir -p /var/www/hub/src/

# Copy the rest of the working directory contents into the container at /app
COPY . . 

# Set script to start Django to be executable
RUN chmod +x run-django.sh