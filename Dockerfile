# Python runtime as parent image
FROM python:2.7.12

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD source/ /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Make port 8800 available to the world outside this container for monitoring
EXPOSE 8080

# Run listener.py when the container launches
CMD ["python", "listener.py", "> slackquotebot.log 2>&1"]

