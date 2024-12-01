FROM python:3.10-slim

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV FLASK_APP app
ENV FLASK_RUN_HOST 0.0.0.0

# Install dependencies
WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source code
COPY . /app

# Run Flask app
CMD ["flask", "run", "--host=0.0.0.0", "--port=3000"]
