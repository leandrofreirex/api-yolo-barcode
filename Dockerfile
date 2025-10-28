# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .


# Install system dependencies
RUN apt-get update && \
    apt-get install libgl1 -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


# Install any needed packages specified in requirements.txt
# We use --no-cache-dir to reduce image size
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application's source code and the model file
COPY main.py .
COPY YOLOV8s_Barcode_Detection.pt .

# Expose port 8000 to the outside world
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
