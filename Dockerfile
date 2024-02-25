FROM python:3.12.2-alpine

WORKDIR /app

# Install requirements
COPY requirements.txt /app
RUN pip3 install -r requirements.txt

# Copy repo
COPY . /app

EXPOSE 5000

# Start application
ENTRYPOINT ["python3"]
CMD ["main.py"]