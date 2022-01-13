# Use Python 3.8 on latest stable version of Debian slim
FROM python:3.8-slim

LABEL maintainer="zacharytbraun@gmail.com"


COPY requirements.txt requirements.txt

# Install the required Python packages
RUN pip install --upgrade pip && pip install -r requirements.txt && \
    # Clean up
    rm requirements.txt

# Add a new user to run the app process instead of root to increase security
RUN useradd app

# Switch to user "app" to run the app process
USER app

WORKDIR /home/app

# Copy the source code to the container
COPY --chown=app src/ ./src
# Copy the dataset to the container (dataset originally from http://2016.padjo.org/files/data/starterpack/cde-schools/cdeschools.sqlite)
COPY --chown=app data/cdeschools.sqlite.z ./src/data/cdeschools.sqlite

CMD [ "gunicorn", "--chdir", "/home/app/src", "--bind", "0.0.0.0:5000", "app:app" ]