# Vercel serverless function entry point for Django
import os
import sys
from pathlib import Path
from io import BytesIO

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'animal_rescue.settings')

# Store setup state
wsgi_application = None
setup_error = None
setup_traceback = None

# Initialize Django application - wrap in try/except to catch all errors
try:
    import django
    django.setup()
    
    from django.core.wsgi import get_wsgi_application
    wsgi_application = get_wsgi_application()
    
except Exception as e:
    import traceback
    setup_error = str(e)
    setup_traceback = traceback.format_exc()
    wsgi_application = None

# Vercel handler function
def handler(request):
    """
    Vercel serverless function handler for Django
    This function will show detailed errors if something fails
    """
    # If Django setup failed, return detailed error
    if wsgi_application is None:
        error_html = f"""
        <html>
        <head><title>Django Setup Error</title></head>
        <body style="font-family: monospace; padding: 20px; background: #f5f5f5;">
            <h1 style="color: #d32f2f;">Django Setup Failed</h1>
            <h2>Error:</h2>
            <pre style="background: white; padding: 15px; border: 1px solid #ddd; overflow-x: auto;">{setup_error}</pre>
            <h2>Full Traceback:</h2>
            <pre style="background: white; padding: 15px; border: 1px solid #ddd; overflow-x: auto; white-space: pre-wrap;">{setup_traceback}</pre>
            <h2>Environment Variables Check:</h2>
            <ul>
                <li>DATABASE_URL: {'SET' if os.environ.get('DATABASE_URL') else '<strong style="color: red;">NOT SET</strong>'}</li>
                <li>SECRET_KEY: {'SET' if os.environ.get('SECRET_KEY') else '<strong style="color: red;">NOT SET</strong>'}</li>
                <li>DEBUG: {os.environ.get('DEBUG', 'Not set')}</li>
                <li>ALLOWED_HOSTS: {os.environ.get('ALLOWED_HOSTS', 'Not set')}</li>
            </ul>
        </body>
        </html>
        """
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'text/html; charset=utf-8'},
            'body': error_html
        }
    
    try:
        # Extract request data - handle different request formats
        if hasattr(request, 'method'):
            method = request.method
        elif isinstance(request, dict):
            method = request.get('method', 'GET')
        else:
            method = 'GET'
        
        if hasattr(request, 'path'):
            path = request.path
        elif isinstance(request, dict):
            path = request.get('path', '/')
        else:
            path = '/'
        
        if hasattr(request, 'query_string'):
            query_string = request.query_string or ''
        elif isinstance(request, dict):
            query_string = request.get('query_string', '') or ''
        else:
            query_string = ''
        
        if hasattr(request, 'headers'):
            headers_dict = request.headers
        elif isinstance(request, dict):
            headers_dict = request.get('headers', {})
        else:
            headers_dict = {}
        
        if hasattr(request, 'body'):
            body_bytes = request.body or b''
        elif isinstance(request, dict):
            body_bytes = request.get('body', b'') or b''
        else:
            body_bytes = b''
        
        # Build WSGI environment
        host = headers_dict.get('host', 'localhost')
        server_name = host.split(':')[0] if ':' in host else host
        
        environ = {
            'REQUEST_METHOD': method,
            'SCRIPT_NAME': '',
            'PATH_INFO': path,
            'QUERY_STRING': query_string,
            'CONTENT_TYPE': headers_dict.get('content-type', ''),
            'CONTENT_LENGTH': str(len(body_bytes)),
            'SERVER_NAME': server_name,
            'SERVER_PORT': '443',
            'SERVER_PROTOCOL': 'HTTP/1.1',
            'wsgi.version': (1, 0),
            'wsgi.url_scheme': 'https',
            'wsgi.input': BytesIO(body_bytes),
            'wsgi.errors': sys.stderr,
            'wsgi.multithread': False,
            'wsgi.multiprocess': True,
            'wsgi.run_once': False,
        }
        
        # Add HTTP headers
        for key, value in headers_dict.items():
            key_upper = key.upper().replace('-', '_')
            if key_upper not in ('CONTENT_TYPE', 'CONTENT_LENGTH'):
                environ[f'HTTP_{key_upper}'] = value
        
        # Call WSGI application
        response_data = {'status': None, 'headers': []}
        
        def start_response(status, response_headers):
            response_data['status'] = status
            response_data['headers'] = response_headers
        
        response_body = wsgi_application(environ, start_response)
        
        # Extract response
        status_code = int(response_data['status'].split()[0])
        response_headers = dict(response_data['headers'])
        body_content = b''.join(response_body)
        
        # Return response in Vercel format
        return {
            'statusCode': status_code,
            'headers': response_headers,
            'body': body_content.decode('utf-8', errors='replace')
        }
        
    except Exception as e:
        import traceback
        error_traceback = traceback.format_exc()
        error_html = f"""
        <html>
        <head><title>Handler Error</title></head>
        <body style="font-family: monospace; padding: 20px; background: #f5f5f5;">
            <h1 style="color: #d32f2f;">Handler Error</h1>
            <h2>Error:</h2>
            <pre style="background: white; padding: 15px; border: 1px solid #ddd; overflow-x: auto;">{str(e)}</pre>
            <h2>Full Traceback:</h2>
            <pre style="background: white; padding: 15px; border: 1px solid #ddd; overflow-x: auto; white-space: pre-wrap;">{error_traceback}</pre>
        </body>
        </html>
        """
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'text/html; charset=utf-8'},
            'body': error_html
        }

