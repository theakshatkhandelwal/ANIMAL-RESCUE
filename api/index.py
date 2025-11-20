# Vercel serverless function entry point
import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'animal_rescue.settings')

try:
    # Import Django
    import django
    django.setup()
    
    from django.core.wsgi import get_wsgi_application
    
    # Get WSGI application
    application = get_wsgi_application()
except Exception as e:
    # If there's an error during setup, create a simple error handler
    import traceback
    error_details = traceback.format_exc()
    
    def error_application(environ, start_response):
        """Error handler if Django setup fails"""
        status = '500 Internal Server Error'
        headers = [('Content-Type', 'text/plain; charset=utf-8')]
        start_response(status, headers)
        error_msg = f"Django setup failed:\n{str(e)}\n\n{error_details}"
        return [error_msg.encode('utf-8')]
    
    application = error_application

# Export for Vercel
# The @vercel/python runtime will automatically detect and use the WSGI application

