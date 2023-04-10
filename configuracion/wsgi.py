"""

Expone el WSGI invocable como una variable de nivel de módulo llamada ``aplicación``.

"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'configuracion.settings')

application = get_wsgi_application()
