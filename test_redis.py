import os
import sys
import django
import redis
from django.conf import settings


sys.path.append(os.path.join(os.path.dirname(__file__), "Django_e_commerce"))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Django_e_commerce.settings")

django.setup()


try:
    r = redis.Redis.from_url(settings.CACHES["default"]["LOCATION"])
    r.ping()
    print("Подключение к Redis успешно!")
except redis.ConnectionError:
    print("Не удалось подключиться к Redis.")
except Exception as e:
    print(f"Произошла ошибка: {e}")
