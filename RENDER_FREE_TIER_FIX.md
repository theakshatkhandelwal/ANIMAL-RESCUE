# 🔧 Fix for Render Free Tier (No Shell Access)

## Problem
Render Free Tier doesn't include Shell access, so you can't run `python manage.py migrate` manually.

## Solution: Run Migrations in Build Command

I've updated the build command to run migrations automatically!

### Update Your Render Settings:

1. Go to Render Dashboard → Your Web Service
2. Click **"Settings"** tab
3. Find **"Build Command"**
4. Change it to:
   ```
   pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate --noinput
   ```
5. Click **"Save Changes"**
6. Render will automatically redeploy

### What This Does:

- `pip install -r requirements.txt` - Installs dependencies
- `python manage.py collectstatic --noinput` - Collects static files
- `python manage.py migrate --noinput` - **Runs migrations automatically!**

## Alternative: Use render.yaml

I've already updated `render.yaml` with the correct build command. If you recreate your service using `render.yaml`, it will use the correct settings automatically.

## After Updating Build Command:

1. Save the changes
2. Wait for automatic redeploy (or trigger manual deploy)
3. Your app should work after migrations run!

## Create Superuser (Optional)

If you need to create a superuser but don't have Shell access:

1. **Option 1**: Use Django admin registration (if you have a registration endpoint)
2. **Option 2**: Upgrade to paid plan for Shell access
3. **Option 3**: Create superuser locally and import data
4. **Option 4**: Use Django's `createsuperuser` via a management command endpoint (advanced)

---

**The main fix is adding migrations to the build command!** ✅

