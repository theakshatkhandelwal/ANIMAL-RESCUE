# 🚨 CRITICAL FIX: Wrong Start Command

## The Problem

Render is trying to run: `gunicorn app:app`
But it should be: `gunicorn animal_rescue.wsgi:application --bind 0.0.0.0:$PORT`

## The Fix

1. Go to your Render Web Service
2. Click **"Settings"** tab
3. Scroll down to **"Start Command"**
4. **Delete** whatever is there
5. **Enter exactly this**:
   ```
   gunicorn animal_rescue.wsgi:application --bind 0.0.0.0:$PORT
   ```
6. Click **"Save Changes"**
7. Render will automatically redeploy

## Verify

After saving, check that the Start Command shows:
```
gunicorn animal_rescue.wsgi:application --bind 0.0.0.0:$PORT
```

**NOT** `gunicorn app:app` or anything else!

## Why This Matters

- `animal_rescue.wsgi:application` is your Django WSGI application
- `--bind 0.0.0.0:$PORT` tells gunicorn to listen on the port Render provides
- Without this, your app won't start!

---

**After fixing this, your app should start successfully!** ✅

