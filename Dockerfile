FROM python:3.11-slim

# Install system dependencies required for Manim and Voiceover
# ffmpeg: for video processing
# sox: for audio processing (manim-voiceover)
# libcairo2-dev, libpango1.0-dev: for Manim graphics
# build-essential: for compiling python packages
RUN apt-get update && apt-get install -y \
    ffmpeg \
    sox \
    libcairo2-dev \
    libpango1.0-dev \
    pkg-config \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose the port Streamlit runs on
EXPOSE 8501

# Command to run the application
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
