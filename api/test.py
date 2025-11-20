# Simple test handler to verify Vercel is working
def handler(request):
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'text/plain'},
        'body': 'Vercel Python handler is working!'
    }

