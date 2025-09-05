# Dockerfile
ARG AIRFLOW_VERSION=2.11.0
ARG PYTHON_VERSION_TAG=3.11 
FROM apache/airflow:${AIRFLOW_VERSION}-python${PYTHON_VERSION_TAG} as base

ARG AIRFLOW_VERSION # Re-declare to be in scope
ARG PYTHON_VERSION_TAG # Re-declare to be in scope

USER root

# This section is optional and can be removed if you don't need to compile certain Python packages.
# It installs common build tools.
# RUN apt-get update -yqq && \
#     apt-get install -yqq --no-install-recommends build-essential && \
#     apt-get clean && rm -rf /var/lib/apt/lists/*

USER airflow

# Copy and install Python dependencies from requirements files
COPY --chown=airflow:airflow requirements.txt requirements-dev.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt && \
    pip install --no-cache-dir -r /tmp/requirements-dev.txt

# The rest of the image setup is handled by the official Airflow entrypoint.
# No need to manually create directories or change ownership here,
# as the airflow-init service and volume mounts handle it.
