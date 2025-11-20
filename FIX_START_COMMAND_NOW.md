# 🚨 URGENT: Fix Start Command in Render

## The Problem

Render is still running: `gunicorn app:app` (WRONG!)
It should be: `gunicorn animal_rescue.wsgi:application --bind 0.0.0.0:$PORT`

## Solution 1: Fix in Render Dashboard (DO THIS NOW!)

1. **Go to Render Dashboard** → Your Web Service
2. Click **"Settings"** tab (left sidebar)
3. Scroll down to **"Start Command"** section
4. **DELETE** everything in the Start Command field
5. **Type exactly this**:
   ```
   gunicorn animal_rescue.wsgi:application --bind 0.0.0.0:$PORT
   ```
6. Click **"Save Changes"** button
7. Render will automatically redeploy

## Solution 2: Use render.yaml (Automatic)

I've created a `render.yaml` file that will auto-configure Render.

1. **Delete your current Web Service** in Render
2. **Create a new Web Service**
3. When connecting your repo, Render should detect `render.yaml`
4. It will use the correct settings automatically

## Verify It's Fixed

After saving, check:
- Go to Settings → Start Command
- It should show: `gunicorn animal_rescue.wsgi:application --bind 0.0.0.0:$PORT`
- **NOT** `gunicorn app:app`

## Why This Keeps Happening

Render might be auto-detecting the wrong command. The `render.yaml` file I created will prevent this.

---

**DO THIS NOW**: Go to Settings → Start Command → Change it to the correct command!

