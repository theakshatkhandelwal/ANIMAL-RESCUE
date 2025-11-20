# Deploy to Render (EASIEST for Django)

Render is the easiest platform for Django. Here's how:

## Step 1: Sign up for Render
1. Go to https://render.com
2. Sign up with GitHub
3. Click "New +" → "Web Service"
4. Connect your `ANIMAL-RESCUE` repository

## Step 2: Configure Service
- **Name**: `animal-rescue` (or your choice)
- **Region**: Choose closest to you
- **Branch**: `main`
- **Root Directory**: (leave empty)
- **Runtime**: `Python 3`
- **Build Command**: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
- **Start Command**: `gunicorn animal_rescue.wsgi:application`

## Step 3: Add PostgreSQL Database
1. In Render Dashboard, click "New +" → "PostgreSQL"
2. Name it: `animal-rescue-db`
3. Copy the "Internal Database URL"

## Step 4: Set Environment Variables
In your Web Service → Environment tab, add:

```
DATABASE_URL=<paste the PostgreSQL Internal Database URL>
SECRET_KEY=8y3UjX18Ejly__IAEz4WCkxoWjYTbxRcYPrIsofPvFEWANdRZjIAWqqcMQCxL01ULfI
DEBUG=False
ALLOWED_HOSTS=*.onrender.com
PYTHON_VERSION=3.12.7
```

## Step 5: Deploy
1. Click "Create Web Service"
2. Render will automatically:
   - Install dependencies
   - Run migrations (you can add this to build command)
   - Start your app

## Step 6: Run Migrations
1. Go to your service → "Shell"
2. Run: `python manage.py migrate`
3. Run: `python manage.py createsuperuser`

## Done! 🎉

Your app will be live at: `https://animal-rescue.onrender.com`

## Why Render is Best:
- ✅ Easiest Django deployment
- ✅ Free PostgreSQL included
- ✅ Automatic HTTPS
- ✅ No complex configuration
- ✅ Free tier available

