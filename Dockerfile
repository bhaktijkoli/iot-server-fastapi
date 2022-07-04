# Set Base Image
FROM python:3.9

# Set Working Dir
WORKDIR /code

# Copy Requirements txt
COPY ./requirements.txt /code/requirements.txt

# Install Dependencies
RUN pip install -r /code/requirements.txt

# Copy Code Files
COPY ./app /code/app

# Copy Cert Files
COPY ./certs /code/certs

# Expose Port
EXPOSE 80

# CMD
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--ssl-keyfile", "./certs/private.key", "--ssl-certfile", "./certs/CA.crt"]