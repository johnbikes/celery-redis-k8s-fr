import os
from pathlib import Path

from celery import Celery


def main():
    # not graceful
    # images_path: Path = os.environ['IMAGES_PATH']
    # assert images_path.is_dir(), f"{images_path} is not a directory"
    image_path: Path = Path(os.environ['IMAGE_PATH'])
    assert image_path.is_file(), f"{image_path} is not a file"

    # Celery app configuration
    # celery = Celery('tasks', broker='redis://redis-server:6379/0')
    # TODO: grab from env
    # celery = Celery('tasks', backend=f"redis://localhost", broker='redis://localhost:6379/0')
    celery = Celery('tasks', backend=f"redis://localhost", broker='redis://localhost:6379')

    results = []
    for i in range(10):
        # can also use apply_async
        result = celery.send_task('fr_tasks.detect_template', args=[str(image_path),], kwargs={})
        results.append(result)

    while len(results) > 0:
        if results[0].ready():
            # TODO: use a deque or a better approach here
            front = results.pop(0)
            r = front.get()
            print(r, type(r))
        

if __name__ == "__main__":
    main()