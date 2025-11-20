# Vercel serverless function entry point for Django
import os
import sys
from pathlib import Path
from io import BytesIO

# Add project root to path - wrap in try/except to avoid crashes
try:
    project_root = Path(__file__).parent.parent
    sys.path.insert(0, str(project_root))
except Exception:
    pass  # Continue even if path setup fails

# Set Django settings module
try:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'animal_rescue.settings')
except Exception:
    pass  # Continue even if env var setup fails

# Cache for WSGI application (lazy loading)
_wsgi_app_cache = None

def get_wsgi_app():
    """Lazy load WSGI application"""
    global _wsgi_app_cache, _import_success, _import_error, _import_traceback
    
    # If imports failed at module level, return that error
    if not _import_success:
        return {
            'error': f'Module import failed: {_import_error}',
            'traceback': _import_traceback
        }
    
    if _wsgi_app_cache is None:
        try:
            import django
            django.setup()
            from django.core.wsgi import get_wsgi_application
            _wsgi_app_cache = get_wsgi_application()
        except Exception as e:
            import traceback
            _wsgi_app_cache = {
                'error': str(e),
                'traceback': traceback.format_exc()
            }
    return _wsgi_app_cache

# Vercel handler function
def handler(request):
    """
    Vercel serverless function handler for Django
    This function will show detailed errors if something fails
    """
    # First, try to understand what type of request object we have
    request_type = type(request).__name__
    request_repr = str(request)[:200] if request else 'None'
    
    # Get WSGI application (lazy loaded)
    wsgi_app_result = get_wsgi_app()
    
    # If Django setup failed, return detailed error
    if isinstance(wsgi_app_result, dict) and 'error' in wsgi_app_result:
        error_html = f"""
        <html>
        <head><title>Django Setup Error</title></head>
        <body style="font-family: monospace; padding: 20px; background: #f5f5f5;">
            <h1 style="color: #d32f2f;">Django Setup Failed</h1>
            <h2>Error:</h2>
            <pre style="background: white; padding: 15px; border: 1px solid #ddd; overflow-x: auto;">{wsgi_app_result['error']}</pre>
            <h2>Full Traceback:</h2>
            <pre style="background: white; padding: 15px; border: 1px solid #ddd; overflow-x: auto; white-space: pre-wrap;">{wsgi_app_result['traceback']}</pre>
            <h2>Environment Variables Check:</h2>
            <ul>
                <li>DATABASE_URL: {'SET' if os.environ.get('DATABASE_URL') else '<strong style="color: red;">NOT SET</strong>'}</li>
                <li>SECRET_KEY: {'SET' if os.environ.get('SECRET_KEY') else '<strong style="color: red;">NOT SET</strong>'}</li>
                <li>DEBUG: {os.environ.get('DEBUG', 'Not set')}</li>
                <li>ALLOWED_HOSTS: {os.environ.get('ALLOWED_HOSTS', 'Not set')}</li>
            </ul>
            <h2>Request Info:</h2>
            <ul>
                <li>Request Type: {request_type}</li>
                <li>Request: {request_repr}</li>
            </ul>
        </body>
        </html>
        """
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'text/html; charset=utf-8'},
            'body': error_html
        }
    
    wsgi_application = wsgi_app_result
    
    try:
        # Try multiple ways to extract request data
        # Method 1: Vercel Request object (has attributes)
        if hasattr(request, 'method'):
            method = request.method
            path = getattr(request, 'path', '/')
            query_string = getattr(request, 'query_string', '') or ''
            headers_dict = getattr(request, 'headers', {}) or {}
            body_bytes = getattr(request, 'body', b'') or b''
        
        # Method 2: Dictionary format
        elif isinstance(request, dict):
            method = request.get('method', 'GET')
            path = request.get('path', request.get('url', '/'))
            query_string = request.get('query_string', request.get('query', '')) or ''
            headers_dict = request.get('headers', {}) or {}
            body_bytes = request.get('body', b'') or b''
            if isinstance(body_bytes, str):
                body_bytes = body_bytes.encode('utf-8')
        
        # Method 3: Try to get from request object attributes
        else:
            # Try common attribute names
            method = getattr(request, 'method', getattr(request, 'httpMethod', 'GET'))
            path = getattr(request, 'path', getattr(request, 'pathname', '/'))
            query_string = getattr(request, 'query_string', getattr(request, 'queryString', '')) or ''
            headers_dict = getattr(request, 'headers', {}) or {}
            body_bytes = getattr(request, 'body', getattr(request, 'rawBody', b'')) or b''
            if isinstance(body_bytes, str):
                body_bytes = body_bytes.encode('utf-8')
        
        # If path is a full URL, extract just the path
        if path.startswith('http'):
            from urllib.parse import urlparse
            parsed = urlparse(path)
            path = parsed.path
            if not query_string and parsed.query:
                query_string = parsed.query
        
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

