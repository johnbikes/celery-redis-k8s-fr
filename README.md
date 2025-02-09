# celery-redis-k8s-fr
- this would be faster with a gpu, especially with batching, but that's not the point of this project
- insightface params are mostly default

## Docker build
- `docker build -t python-celery .`

## Docker run
- `docker run -it --rm python-celery`

## With compose
- just build
  - `docker compose build`
- `docker compose up` # -d to detach # --build

## k8s
- apply
- expose