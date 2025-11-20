# Deploy to Railway (EASIER than Vercel for Django)

Railway is much better for Django apps. Here's how to deploy:

## Step 1: Sign up for Railway
1. Go to https://railway.app
2. Sign up with GitHub
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Choose your `ANIMAL-RESCUE` repository

## Step 2: Add PostgreSQL Database
1. In Railway project, click "+ New"
2. Select "Database" → "Add PostgreSQL"
3. Railway will create a PostgreSQL database automatically

## Step 3: Set Environment Variables
In Railway project → Variables tab, add:

```
DATABASE_URL=${{Postgres.DATABASE_URL}}
SECRET_KEY=8y3UjX18Ejly__IAEz4WCkxoWjYTbxRcYPrIsofPvFEWANdRZjIAWqqcMQCxL01ULfI
DEBUG=False
ALLOWED_HOSTS=*.railway.app
```

Railway automatically sets `DATABASE_URL` from the PostgreSQL service!

## Step 4: Configure Build Settings
Railway will auto-detect Django, but you can set:
- **Build Command**: (leave empty, auto-detected)
- **Start Command**: `python manage.py migrate && gunicorn animal_rescue.wsgi:application --bind 0.0.0.0:$PORT`

## Step 5: Deploy
Railway will automatically:
1. Install dependencies from `requirements.txt`
2. Run migrations
3. Start your app

## Step 6: Create Superuser
1. Go to Railway project → Deployments
2. Click on your deployment → "View Logs"
3. Click "Open Shell"
4. Run: `python manage.py createsuperuser`

## Done! 🎉

Your app will be live at: `https://your-app-name.railway.app`

## Why Railway is Better:
- ✅ Built for Django/Python
- ✅ Automatic PostgreSQL setup
- ✅ No handler function needed
- ✅ Standard WSGI deployment
- ✅ Free tier available
- ✅ Much simpler!

