#!/usr/bin/env python
"""
Quick diagnostic script to check deployment issues
Run this in Render Shell: python check_deployment.py
"""
import os
import sys

print("=" * 60)
print("DEPLOYMENT DIAGNOSTIC CHECK")
print("=" * 60)

# Check environment variables
print("\n1. Environment Variables:")
env_vars = ['DATABASE_URL', 'SECRET_KEY', 'DEBUG', 'ALLOWED_HOSTS', 'PYTHON_VERSION']
for var in env_vars:
    value = os.environ.get(var, 'NOT SET')
    if var == 'DATABASE_URL' and value != 'NOT SET':
        # Hide password in output
        if '@' in value:
            parts = value.split('@')
            if len(parts) == 2:
                user_pass = parts[0].split('://')[-1]
                if ':' in user_pass:
                    user = user_pass.split(':')[0]
                    value = value.replace(user_pass, f'{user}:***')
    print(f"   {var}: {value}")

# Check Django setup
print("\n2. Django Setup:")
try:
    import django
    print(f"   Django version: {django.get_version()}")
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'animal_rescue.settings')
    django.setup()
    print("   ✅ Django setup successful")
except Exception as e:
    print(f"   ❌ Django setup failed: {e}")
    sys.exit(1)

# Check database connection
print("\n3. Database Connection:")
try:
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
    print("   ✅ Database connection successful")
except Exception as e:
    print(f"   ❌ Database connection failed: {e}")
    print("   This is likely the issue! Check DATABASE_URL is set correctly.")

# Check if migrations are needed
print("\n4. Database Migrations:")
try:
    from django.core.management import call_command
    from io import StringIO
    out = StringIO()
    call_command('showmigrations', '--plan', stdout=out)
    migrations = out.getvalue()
    if '[ ]' in migrations:
        print("   ⚠️  Some migrations are not applied!")
        print("   Run: python manage.py migrate")
    else:
        print("   ✅ All migrations applied")
except Exception as e:
    print(f"   ⚠️  Could not check migrations: {e}")

# Check models
print("\n5. Models Check:")
try:
    from django.apps import apps
    models = apps.get_models()
    print(f"   ✅ Found {len(models)} models")
except Exception as e:
    print(f"   ❌ Error loading models: {e}")

print("\n" + "=" * 60)
print("DIAGNOSTIC COMPLETE")
print("=" * 60)
print("\nIf database connection failed, check:")
print("1. DATABASE_URL is set in Render Environment Variables")
print("2. PostgreSQL database is 'Available' (not paused)")
print("3. Run: python manage.py migrate")
print("\n")

