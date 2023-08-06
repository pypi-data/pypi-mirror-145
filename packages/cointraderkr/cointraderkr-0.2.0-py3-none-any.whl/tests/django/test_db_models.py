from unittest import TestCase

# Django related imports
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings')
application = get_wsgi_application()

from db.models import *


class TestDbModelsClass(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass