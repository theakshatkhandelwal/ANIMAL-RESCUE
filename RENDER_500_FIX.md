# 🔧 Fix 500 Server Error on Render

## Step 1: Run Diagnostic Script

First, let's see what's wrong:

1. Go to Render Dashboard → Your Web Service
2. Click **"Shell"** tab
3. Run:
   ```bash
   python check_deployment.py
   ```
4. This will show you exactly what's wrong

## Step 2: Fix Based on Diagnostic

### If Database Connection Failed:
1. Go to Render → Environment Variables
2. Check `DATABASE_URL` is set
3. Make sure PostgreSQL database is "Available" (not paused)
4. Copy the Internal Database URL from PostgreSQL service
5. Set it in Web Service → Environment → `DATABASE_URL`

### If Migrations Not Run (MOST COMMON!):

**Fix:**
1. Go to Render Dashboard → Your Web Service
2. Click **"Shell"** tab (left sidebar)
3. Run:
   ```bash
   python manage.py migrate
   ```
4. Wait for migrations to complete
5. Refresh your app

### 2. Missing Environment Variables

**Check these are set in Render → Environment:**
- ✅ `DATABASE_URL` - Should be set automatically from PostgreSQL
- ✅ `SECRET_KEY` - Must be set
- ✅ `DEBUG` - Should be `False`
- ✅ `ALLOWED_HOSTS` - Should be `*`
- ✅ `PYTHON_VERSION` - Should be `3.12.7`

### 3. Database Connection Issue

**Check:**
1. Go to Render → Your PostgreSQL Database
2. Make sure it's **"Available"** (not paused)
3. Copy the **Internal Database URL**
4. Verify it's set in Web Service → Environment → `DATABASE_URL`

### 4. Check Logs for Exact Error

**To see the actual error:**
1. Go to Render Dashboard → Your Web Service
2. Click **"Logs"** tab
3. Look for error messages (usually in red or with "ERROR" or "Exception")
4. The error message will tell you exactly what's wrong

## Quick Fix Steps

1. **Run Migrations** (most important!):
   ```bash
   # In Render Shell
   python manage.py migrate
   ```

2. **Create Superuser** (optional but recommended):
   ```bash
   # In Render Shell
   python manage.py createsuperuser
   ```

3. **Check Logs** for specific error messages

4. **Verify Environment Variables** are all set

## Most Likely Issue: Migrations!

If you haven't run migrations yet, that's almost certainly the problem. Run:
```bash
python manage.py migrate
```

---

**After running migrations, your app should work!** ✅

