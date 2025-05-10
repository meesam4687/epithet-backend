# Use an official lightweight Python image
FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy everything to the container
COPY . /app

# Install dependencies
RUN pip install -r requirements.txt
RUN pip install --no-cache-dir flask flask_cors gunicorn requests

# Run pre-deploy script to download the model
RUN python predeploy.py

# Expose port 7860 (Hugging Face Spaces default)
EXPOSE 7860

# Run the Flask app with optimized gunicorn settings
CMD ["gunicorn", "--workers=2", "--threads=2", "--timeout=600", "-b", "0.0.0.0:7860", "main:app"]

