# по умолчанию
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quotes_of_the_day.settings')
application = get_asgi_application()