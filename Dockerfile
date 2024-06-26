# Dockerfile

# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /user_management-main

# Copy the current directory contents into the container at /user_management-main
COPY . /user_management-main

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r /user_management-main/requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV FLASK_APP=run.py

# Run app.py when the container launches
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
