# Use an official Python runtime as the base image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install -r requirements.txt

# Copy the Django project files to the container
COPY . .

# Change directory to time_series_forecaster
WORKDIR /app/time_series_forecaster

# Run Make migrations
RUN python manage.py makemigrations

# Run Migrate
RUN python manage.py migrate

# Run the command to populate the dataset
RUN python manage.py populatedataset

# Expose the necessary port(s) for the Django app
EXPOSE 8000

# Set the entrypoint command to run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

