import os

import django
from channels.http import AsgiHandler
from channels.routing import ProtocolTypeRouter

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'configuracion.settings')
django.setup()

application = ProtocolTypeRouter({
  "http": AsgiHandler(),
# Solo HTTP por ahora. (Podemos agregar otros protocolos más adelante).
})
