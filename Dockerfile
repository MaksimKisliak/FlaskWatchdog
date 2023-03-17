# Use the official Python 3.11 image as the base
FROM python:3.11

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install dependencies using pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Set the environment variable for Flask to run the application
ENV FLASK_APP=run.py

# Expose the port the application will run on
EXPOSE 5000

# Start the application using the Flask development server
CMD ["flask", "run", "--host", "0.0.0.0"]
