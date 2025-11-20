# Ultra-simple test handler - minimal code to avoid any import issues
# Try multiple handler formats that Vercel might expect

def handler(request):
    """Main handler function"""
    try:
        # Handle None request
        if request is None:
            request = {}
        
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'text/html; charset=utf-8'},
            'body': '<h1>✅ Vercel Python Works!</h1><p>Handler is functioning correctly.</p>'
        }
    except Exception as e:
        import traceback
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'text/html; charset=utf-8'},
            'body': f'<h1>Error</h1><pre>{str(e)}\n{traceback.format_exc()}</pre>'
        }

# Alternative export format (some Vercel setups expect this)
__all__ = ['handler']

