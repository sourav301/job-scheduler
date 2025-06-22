FROM python:3.11-slim

# Set work directory
WORKDIR /code

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY ./src /code/src

# Start uvicorn server
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
