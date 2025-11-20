# Vercel serverless function entry point
import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'animal_rescue.settings')

# Import Django application
import django
django.setup()

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

# Vercel handler
def handler(request):
    return application(request)

