FROM python:3.9

# The size of each of those files
ARG PRODUCER_PROTOCOL="http"
ARG PRODUCER_PATH="/files"
ARG PRODUCER_HOST
ARG PRODUCER_PORT

# Environment variable to help limit batch sizes dynamically without rebuilding
ENV APP_PRODUCER_PROTOCOL=${PRODUCER_PROTOCOL}
ENV APP_PRODUCER_HOST=${PRODUCER_HOST}
ENV APP_PRODUCER_PATH=${PRODUCER_PATH}
ENV APP_PRODUCER_PORT=${PRODUCER_PORT}

# Change the workdir to something specific
WORKDIR /app

# Copy the Python app and install all dependencies
COPY requirements.txt .
COPY ./*.py ./
RUN pip install -r requirements.txt

# Run the server when the container starts
CMD ["python", "main.py"]