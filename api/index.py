# Minimal Vercel handler for Django
def handler(request):
    try:
        import os
        import sys
        from pathlib import Path
        from io import BytesIO
        
        # Setup path
        project_root = Path(__file__).parent.parent
        sys.path.insert(0, str(project_root))
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'animal_rescue.settings')
        
        # Setup Django
        import django
        django.setup()
        from django.core.wsgi import get_wsgi_application
        app = get_wsgi_application()
        
        # Get request info
        method = getattr(request, 'method', 'GET')
        path = getattr(request, 'path', '/')
        headers = getattr(request, 'headers', {})
        body = getattr(request, 'body', b'') or b''
        
        # Build WSGI environ
        environ = {
            'REQUEST_METHOD': method,
            'PATH_INFO': path,
            'QUERY_STRING': '',
            'CONTENT_TYPE': headers.get('content-type', ''),
            'CONTENT_LENGTH': str(len(body)),
            'SERVER_NAME': 'localhost',
            'SERVER_PORT': '443',
            'wsgi.version': (1, 0),
            'wsgi.url_scheme': 'https',
            'wsgi.input': BytesIO(body),
            'wsgi.errors': sys.stderr,
            'wsgi.multithread': False,
            'wsgi.multiprocess': True,
            'wsgi.run_once': False,
        }
        
        # Add headers
        for k, v in headers.items():
            environ[f'HTTP_{k.upper().replace("-", "_")}'] = v
        
        # Call WSGI app
        response_data = {}
        def start_response(status, headers):
            response_data['status'] = status
            response_data['headers'] = headers
        
        body_parts = app(environ, start_response)
        body_content = b''.join(body_parts)
        
        return {
            'statusCode': int(response_data['status'].split()[0]),
            'headers': dict(response_data['headers']),
            'body': body_content.decode('utf-8', errors='replace')
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'text/html'},
            'body': f'<h1>Error</h1><pre>{str(e)}</pre>'
        }
