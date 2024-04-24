import time
from celery import Celery

app = Celery(
    'task',
    broker="redis://localhost:6379/1"
)

@app.task
def kun_add(x,y) -> float:
    print('enter kunAdd...')
    time.sleep(5)
    return x+y
