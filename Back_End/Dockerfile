# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the Flask app files into the working directory
COPY . .

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 80

# Define the command to run the app
CMD ["python", "twitterapi.py"]