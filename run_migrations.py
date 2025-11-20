#!/usr/bin/env python
"""
Script to run migrations on Neon PostgreSQL database
Run this after setting DATABASE_URL environment variable
"""
import os
import sys
import django

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'animal_rescue.settings')

# Setup Django
django.setup()

from django.core.management import execute_from_command_line

if __name__ == '__main__':
    # Check if DATABASE_URL is set
    if not os.environ.get('DATABASE_URL'):
        print("ERROR: DATABASE_URL environment variable is not set!")
        print("\nSet it using:")
        print("Windows PowerShell:")
        print('  $env:DATABASE_URL="postgresql://neondb_owner:npg_Xm6ksJTFyIA3@ep-red-pine-ah2qenfa-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"')
        print("\nWindows CMD:")
        print('  set DATABASE_URL=postgresql://neondb_owner:npg_Xm6ksJTFyIA3@ep-red-pine-ah2qenfa-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require')
        print("\nLinux/Mac:")
        print('  export DATABASE_URL="postgresql://neondb_owner:npg_Xm6ksJTFyIA3@ep-red-pine-ah2qenfa-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"')
        sys.exit(1)
    
    print("Running migrations on Neon database...")
    print(f"Database: {os.environ.get('DATABASE_URL', 'Not set')[:50]}...")
    print()
    
    # Run migrations
    execute_from_command_line(['manage.py', 'migrate'])
    
    print("\n✅ Migrations completed!")
    print("\nNext steps:")
    print("1. Create a superuser: python manage.py createsuperuser")
    print("2. Deploy to Vercel (migrations will be needed there too)")

