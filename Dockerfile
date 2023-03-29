# Use the official Python base image
FROM python:3.9-slim-buster

# Set the working directory
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the .env.development file into the container
COPY .env.development /app/.env

# Copy the rest of the application files into the container
COPY . .

# Expose the port that the app will run on
EXPOSE 5000

# Define environment variable
ENV NAME World

LABEL maintainer="Maksim Kisliak <makskislyak@gmail.com>"

# Start the Gunicorn server
CMD ["gunicorn", "--config", "gunicorn.py", "run:app"]
