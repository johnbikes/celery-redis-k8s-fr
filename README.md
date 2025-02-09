# celery-redis-k8s-fr
- this would be faster with a gpu, especially with batching, but that's not the point of this project
- insightface params are mostly default

## Before running
- update **SOME_IMAGE_FILE.jpg** in the **Dockerfile**
- set **IMAGE_PATH** to this in your env when running **client.py**

## Docker build
- `docker build -t python-celery .`

## Docker run
- `docker run -it --rm python-celery`

## With compose
- just build
  - `docker compose build`
- `docker compose up` # -d to detach # --build

## k8s - IN PROGRESS
- apply
- expose