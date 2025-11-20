# Simple test handler to verify Vercel Python runtime works
def handler(request):
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'text/html'},
        'body': '<h1>Vercel Python Handler Works!</h1><p>If you see this, the basic handler is working.</p>'
    }

