# Use an appropriate Python base image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /

# Copy your Python script into the container
COPY . .

# Install any dependencies your script requires (if any)
RUN pip install -r requirements.txt

# Command to run the Python script when the container starts
CMD ["python", "main.py"]
