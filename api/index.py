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

# Initialize Django application
try:
    import django
    django.setup()
    
    from django.core.wsgi import get_wsgi_application
    wsgi_application = get_wsgi_application()
    
    # Flag to track if setup was successful
    django_setup_success = True
except Exception as e:
    django_setup_success = False
    setup_error = str(e)
    import traceback
    setup_traceback = traceback.format_exc()

# Vercel handler function
def handler(request):
    """
    Vercel serverless function handler for Django
    """
    # If Django setup failed, return error immediately
    if not django_setup_success:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'text/plain; charset=utf-8'},
            'body': f"Django setup failed:\n{setup_error}\n\n{setup_traceback}"
        }
    
    try:
        # Extract request data
        method = getattr(request, 'method', 'GET')
        path = getattr(request, 'path', '/')
        query_string = getattr(request, 'query_string', '') or ''
        headers_dict = getattr(request, 'headers', {})
        body_bytes = getattr(request, 'body', b'') or b''
        
        # Build WSGI environment
        environ = {
            'REQUEST_METHOD': method,
            'SCRIPT_NAME': '',
            'PATH_INFO': path,
            'QUERY_STRING': query_string,
            'CONTENT_TYPE': headers_dict.get('content-type', ''),
            'CONTENT_LENGTH': str(len(body_bytes)),
            'SERVER_NAME': headers_dict.get('host', 'localhost').split(':')[0] if headers_dict.get('host') else 'localhost',
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
        error_msg = f"Handler error: {str(e)}\n{traceback.format_exc()}"
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'text/plain; charset=utf-8'},
            'body': error_msg
        }

