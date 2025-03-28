# Use the official Python image from Docker Hub
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install dependencies listed in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY *.py /app/
COPY templates/*.html /app/templates/
COPY static/*.* /app/static/

# Set the environment variable to tell Flask that it is running in production
ENV FLASK_ENV=production

# Define the command to run the app
CMD ["python", "api.py"]
