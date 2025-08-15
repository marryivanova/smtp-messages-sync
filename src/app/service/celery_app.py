from celery import Celery

app = Celery(
    "src.service.celery_app",
    broker="amqp://guest:guest@localhost:5672//",
    backend="rpc://",
    include=["src.service.tasks"],
    broker_connection_retry_on_startup=True,
)