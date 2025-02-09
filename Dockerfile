FROM ubuntu:24.04

# Set the working directory to /app
WORKDIR /app

# Install Python 3.12
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y python3.12 \
    python3.12-dev python3.12-venv python3-pip

# for opencv
RUN apt-get update && apt-get install -y libgl1 libglib2.0-0

# tmp: using --break-system-packages to avoid venv through Dockerfile/sh
RUN python3.12 -m pip install celery==5.4.0 redis==5.2.1 insightface==0.7.3 onnxruntime==1.20.0 --break-system-packages 
RUN python3.12 -m pip install opencv-python==4.11.0.86 --break-system-packages

COPY buffalo_l.zip /root/.insightface/models/buffalo_l.zip
RUN apt-get install -y unzip
RUN mkdir -p /root/.insightface/models && cd /root/.insightface/models && unzip buffalo_l.zip -d buffalo_l && rm buffalo_l.zip

# TODO: necessary
# COPY SOME_IMAGE_FILE.jpg .

COPY fr_tasks.py .

# Run the command to start Celery worker
CMD ["celery", "-A", "fr_tasks", "worker", "--loglevel=INFO"]
