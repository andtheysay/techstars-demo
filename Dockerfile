# Use Python 3.8 on latest stable version of Debian slim
FROM python:3.8-slim

LABEL maintainer="zacharytbraun@gmail.com"

# Get the wheel file to install app
ADD src/dist/flask_app-0.1.0-py3-none-any.whl ./

# Install the required Python packages
RUN pip install --no-cache-dir pip --upgrade && pip install --no-cache-dir *.whl && \
    # Clean up
    rm flask_app-0.1.0-py3-none-any.whl && \
    # Add a new user to run the app process instead of root to increase security
    useradd app

# Switch to user "app" to run the app process
USER app

# Get the dataset (dataset originally from http://2016.padjo.org/files/data/starterpack/cde-schools/cdeschools.sqlite)
ADD --chown=app https://drive.google.com/file/d/1d2vwG2eETdiRB-UWumVLW25efzmU-8Sd/view?usp=sharing data/cdeschools.sqlite

# Copy the source code to the container
COPY --chown=app src/flask_app ./

CMD [ "gunicorn", "--bind", "0.0.0.0:5000", "app:app" ]