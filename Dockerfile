# Use the official TensorFlow base image
FROM tensorflow/tensorflow:2.16.1-gpu

# Set environment variables to prevent Python from writing .pyc files and to buffer stdout and stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies including OpenGL libraries and GLib
RUN apt-get update && \
    apt-get install -y libgl1-mesa-glx libglib2.0-0 python3-venv && \
    rm -rf /var/lib/apt/lists/*

# Create and set the working directory
WORKDIR /app

# Create a virtual environment
RUN python3 -m venv /opt/venv

# Ensure all following commands use the virtual environment
ENV PATH="/opt/venv/bin:$PATH"

# Activate the virtual environment and install required packages
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the working directory
COPY . .

# Set environment variable for LD_LIBRARY_PATH to include the directory with libGL.so.1
ENV LD_LIBRARY_PATH=/usr/lib/x86_64-linux-gnu:$LD_LIBRARY_PATH

# Expose the port that the Flask app will run on
EXPOSE 5000

# Ensure the app script is executable
RUN chmod +x app/app.py

# Command to run the Flask app
CMD ["python", "app/app.py"]