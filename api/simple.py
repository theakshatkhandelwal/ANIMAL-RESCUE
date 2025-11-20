# Simple test handler to verify Vercel Python runtime works
def handler(request):
    # Debug: show what type of request we're getting
    request_info = {
        'type': str(type(request)),
        'has_method': hasattr(request, 'method'),
        'is_dict': isinstance(request, dict),
        'request_str': str(request)[:500] if request else 'None'
    }
    
    body = f"""
    <html>
    <head><title>Vercel Test</title></head>
    <body style="font-family: monospace; padding: 20px;">
        <h1>✅ Vercel Python Handler Works!</h1>
        <p>If you see this, the basic handler is working.</p>
        <h2>Request Info:</h2>
        <pre>{request_info}</pre>
    </body>
    </html>
    """
    
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'text/html; charset=utf-8'},
        'body': body
    }

