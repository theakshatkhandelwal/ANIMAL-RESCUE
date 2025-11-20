# 🚀 Deploy to Render - Step by Step Guide

Render is the **EASIEST** platform for Django apps. Follow these steps:

## 📋 Prerequisites
- ✅ Your code is on GitHub (already done!)
- ✅ You have a GitHub account
- ✅ 10 minutes of time

---

## Step 1: Sign Up for Render

1. Go to **https://render.com**
2. Click **"Get Started for Free"**
3. Sign up with your **GitHub account** (easiest way)
4. Authorize Render to access your GitHub

---

## Step 2: Create PostgreSQL Database

1. In Render Dashboard, click **"New +"** button (top right)
2. Select **"PostgreSQL"**
3. Configure:
   - **Name**: `animal-rescue-db` (or any name you like)
   - **Database**: `animal_rescue` (or leave default)
   - **User**: (auto-generated)
   - **Region**: Choose closest to you
   - **PostgreSQL Version**: 15 (or latest)
   - **Plan**: Free (or paid if you need more)
4. Click **"Create Database"**
5. **IMPORTANT**: Wait for database to be created (takes 1-2 minutes)
6. Once created, click on your database
7. Go to **"Connections"** tab
8. Copy the **"Internal Database URL"** - you'll need this!

---

## Step 3: Create Web Service

1. In Render Dashboard, click **"New +"** button
2. Select **"Web Service"**
3. Connect your GitHub repository:
   - If prompted, authorize Render to access your repos
   - Search for: `ANIMAL-RESCUE` (or your repo name)
   - Click **"Connect"** on your repository

---

## Step 4: Configure Web Service

Fill in these settings:

### Basic Settings:
- **Name**: `animal-rescue` (or your choice)
- **Region**: Same as your database
- **Branch**: `main`
- **Root Directory**: (leave empty)
- **Runtime**: `Python 3`
- **Build Command**: 
  ```
  pip install -r requirements.txt && python manage.py collectstatic --noinput
  ```
- **Start Command**: 
  ```
  gunicorn animal_rescue.wsgi:application --bind 0.0.0.0:$PORT
  ```
  
  ⚠️ **CRITICAL**: Make sure the start command is EXACTLY:
  ```
  gunicorn animal_rescue.wsgi:application --bind 0.0.0.0:$PORT
  ```
  
  **NOT** `gunicorn app:app` (this is wrong!)

### Environment Variables:
Click **"Advanced"** → **"Add Environment Variable"** and add these:

1. **DATABASE_URL**
   - Key: `DATABASE_URL`
   - Value: Paste the **Internal Database URL** you copied from Step 2
   - Example: `postgresql://user:password@dpg-xxxxx-a.oregon-postgres.render.com/animal_rescue`

2. **SECRET_KEY**
   - Key: `SECRET_KEY`
   - Value: `8y3UjX18Ejly__IAEz4WCkxoWjYTbxRcYPrIsofPvFEWANdRZjIAWqqcMQCxL01ULfI`

3. **DEBUG**
   - Key: `DEBUG`
   - Value: `False`

4. **ALLOWED_HOSTS**
   - Key: `ALLOWED_HOSTS`
   - Value: `*.onrender.com`

5. **PYTHON_VERSION** (IMPORTANT - use 3.12, not 3.13)
   - Key: `PYTHON_VERSION`
   - Value: `3.12.7`

### Plan:
- Select **"Free"** plan (or paid if you need more resources)

---

## Step 5: Deploy!

1. Click **"Create Web Service"** at the bottom
2. Render will automatically:
   - Clone your repository
   - Install dependencies from `requirements.txt`
   - Build your app
   - Start the service

3. **Wait 5-10 minutes** for first deployment (it's building everything)

---

## Step 6: Run Database Migrations

Once deployment is complete:

1. Go to your Web Service dashboard
2. Click on **"Shell"** tab (in the left sidebar)
3. In the shell, run:
   ```bash
   python manage.py migrate
   ```
4. Wait for migrations to complete
5. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```
   - Enter username, email, and password when prompted

---

## Step 7: Access Your App! 🎉

1. Your app URL will be: `https://animal-rescue.onrender.com` (or your custom name)
2. Click the URL in Render dashboard to open your app
3. You should see your Animal Rescue homepage!

---

## ✅ Verify Everything Works

1. **Homepage**: Visit your app URL - should show the landing page
2. **Admin Panel**: Visit `https://your-app.onrender.com/admin/` - login with superuser
3. **Register**: Try creating a new user account
4. **Database**: Check that data is being saved

---

## 🔧 Troubleshooting

### Issue: "Application Error"
- **Solution**: Check the "Logs" tab in Render dashboard for error messages
- Common causes: Missing environment variables, database connection issues

### Issue: "Static files not loading"
- **Solution**: Make sure `collectstatic` ran in build command
- Check that `whitenoise` is in `requirements.txt` (it is!)

### Issue: "Database connection failed"
- **Solution**: 
  - Verify `DATABASE_URL` is set correctly
  - Make sure database is in same region as web service
  - Check database is "Available" (not paused)

### Issue: "502 Bad Gateway"
- **Solution**: 
  - Check "Logs" for errors
  - Verify `gunicorn` is in `requirements.txt` (it is!)
  - Make sure start command is correct

### Issue: Migrations not running
- **Solution**: Run manually in Shell:
  ```bash
  python manage.py migrate
  ```

---

## 📝 Important Notes

1. **Free Tier Limitations**:
   - Services spin down after 15 minutes of inactivity
   - First request after spin-down takes ~30 seconds
   - Database has 90-day retention on free tier

2. **Custom Domain** (Optional):
   - Go to Settings → Custom Domain
   - Add your domain
   - Update `ALLOWED_HOSTS` to include your domain

3. **Environment Variables**:
   - Never commit sensitive data to GitHub
   - Always use Render's environment variables

4. **Updates**:
   - Push to `main` branch = automatic redeploy
   - Render will rebuild and redeploy automatically

---

## 🎯 Quick Checklist

- [ ] Signed up for Render
- [ ] Created PostgreSQL database
- [ ] Copied Internal Database URL
- [ ] Created Web Service
- [ ] Set all 5 environment variables
- [ ] Deployment completed successfully
- [ ] Ran migrations in Shell
- [ ] Created superuser
- [ ] App is accessible and working!

---

## 🆘 Need Help?

If you get stuck:
1. Check the "Logs" tab in Render dashboard
2. Check "Events" tab to see deployment progress
3. Verify all environment variables are set
4. Make sure database is running

**Your app should be live in about 10-15 minutes!** 🚀

