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

# Get the dataset (dataset originally from http://2016.padjo.org/files/data/starterpack/cde-schools/cdeschools.sqlite)
# https://drive.google.com/file/d/1d2vwG2eETdiRB-UWumVLW25efzmU-8Sd/view?usp=sharing
ADD --chown=app http://2016.padjo.org/files/data/starterpack/cde-schools/cdeschools.sqlite data/cdeschools.sqlite

# Copy the source code to the container
COPY --chown=app src/ ./

CMD [ "gunicorn", "--bind", "0.0.0.0:5000", "app:app" ]