FROM python:3.10

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8000 for the web application
EXPOSE 8000

# Set the environment variable for the web application
ENV PYTHONUNBUFFERED=1

# Start the web application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
