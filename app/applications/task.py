import time

from celery import shared_task


@shared_task()
def call_background_task(
    message: str,
    ) -> None:
    """
    Функция обработчик синхронных задач
    """
    time.sleep(10)
    print("Background Task called!")
    print(message)
