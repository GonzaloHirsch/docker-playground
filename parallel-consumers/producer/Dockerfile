FROM python:3.9

# Number of files that will be created
ARG FILE_COUNT=1000

# The size of each of those files
ARG FILE_SIZE=10240

# The amount of files to send in each batch
ARG BATCH_SIZE=200

# The port to be exposed
ARG APP_PORT=5000

# Environment variable to simplify changing the build directory
ENV FILE_LOCATION=/app/content

# Environment variable to help limit batch sizes dynamically without rebuilding
ENV APP_BATCH_SIZE=${BATCH_SIZE}
ENV APP_FILE_COUNT=${FILE_COUNT}

# Change the workdir to something specific
WORKDIR /app

# Create a directory where the content will live
RUN mkdir -p ${FILE_LOCATION}

# Must copy the generator and grant it permissions
COPY generator.sh .
RUN chmod u+x generator.sh

# Actually running the generation for the files for reproducibility
RUN ./generator.sh -f ${FILE_COUNT} -s ${FILE_SIZE} -p ${FILE_LOCATION}

# Debug the locations
RUN ls ${FILE_LOCATION}

# Copy the Python app and install all dependencies
COPY requirements.txt .
COPY ./*.py ./
RUN pip install --no-cache-dir --upgrade -r requirements.txt

EXPOSE ${APP_PORT}

ENV APP_PORT=${APP_PORT}

# Run the server when the container starts
# Equivalent: export APP_BATCH_SIZE=5; export APP_FILE_COUNT=30; export FILE_LOCATION=./content; uvicorn main:app --host 0.0.0.0 --port 3000
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port $APP_PORT"]