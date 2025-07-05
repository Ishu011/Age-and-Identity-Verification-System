FROM python:3.10-slim

# System dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy files
COPY . /app

# Install dependencies
RUN pip install --upgrade pip
RUN pip install tensorflow-cpu==2.10.1
RUN pip install -r requirements.txt

# Expose port
EXPOSE 5000

# Run the app
CMD ["gunicorn", "backend.app:app", "--bind", "0.0.0.0:5000"]
