# Base image
FROM python:3.11-slim

# Set environment variables to prevent Python from writing .pyc files and buffering stdout and stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV POETRY_VIRTUALENVS_CREATE=false

# Set the working directory
WORKDIR /app

# Install Poetry
RUN pip install poetry

# Copy pyproject.toml and poetry.lock files to the working directory
COPY pyproject.toml poetry.lock /app/

# Install dependencies
RUN poetry install

# Copy the entire project to the working directory
COPY . /app

# Expose the port FastAPI will run on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
