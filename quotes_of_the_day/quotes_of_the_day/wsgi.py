# по умолчанию
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quotes_of_the_day.settings')
application = get_wsgi_application()