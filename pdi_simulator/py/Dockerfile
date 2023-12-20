# Use the official Ubuntu image as a parent image
FROM ubuntu:latest

# Set the working directory in the container
WORKDIR /app

# Update the package list and install necessary packages
RUN apt-get update -y && \
    apt-get install -y python3 python3-pip

# Copy the contents of the local directory to the container's /app directory
COPY . /app
COPY ./templates /app/templates

# Install any needed Python packages
RUN pip3 install -r requirements.txt

# Expose ports 5000 and 5001 for Flask
EXPOSE 5000
EXPOSE 5001

# Run main.py when the container launches, specify the port using the environment variable
CMD ["python3", "main.py"]
