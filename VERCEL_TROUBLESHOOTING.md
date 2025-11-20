# Vercel Deployment Troubleshooting Guide

## Current Issue: Function Crashes with 500 Error

### Step 1: Test Basic Handler First

After redeploy, test the simple handler:
- Visit: `https://animal-rescue-adoption.vercel.app/test`
- If this works → Python runtime is OK, issue is with Django
- If this fails → Issue is with Vercel Python runtime setup

### Step 2: Check Vercel Function Logs

**CRITICAL:** This will show the actual error!

1. Go to Vercel Dashboard
2. Click your project
3. Click "Functions" tab
4. Click on `api/index.py`
5. Click "Logs" tab
6. Look for error messages

**Share the error message from the logs!**

### Step 3: Verify Environment Variables

In Vercel Dashboard → Settings → Environment Variables, ensure ALL are set:

```
DATABASE_URL=postgresql://neondb_owner:npg_Xm6ksJTFyIA3@ep-red-pine-ah2qenfa-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require

SECRET_KEY=8y3UjX18Ejly__IAEz4WCkxoWjYTbxRcYPrIsofPvFEWANdRZjIAWqqcMQCxL01ULfI

DEBUG=False

ALLOWED_HOSTS=*.vercel.app
```

**Important:**
- Make sure they're set for "Production" environment
- After adding/changing, you MUST redeploy

### Step 4: Check Database Connection

Verify migrations ran successfully:
1. Go to Neon Dashboard
2. Open SQL Editor
3. Run: `SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';`
4. Should return a number > 0 (at least 20+ tables)

### Step 5: Common Issues

#### Issue: "ModuleNotFoundError"
- **Cause:** Missing dependency
- **Fix:** Check `requirements.txt` includes all packages

#### Issue: "Database connection failed"
- **Cause:** DATABASE_URL not set or wrong
- **Fix:** Verify environment variable in Vercel

#### Issue: "SECRET_KEY not set"
- **Cause:** Missing SECRET_KEY
- **Fix:** Add SECRET_KEY environment variable

#### Issue: "ALLOWED_HOSTS"
- **Cause:** Domain not in ALLOWED_HOSTS
- **Fix:** Set ALLOWED_HOSTS=*.vercel.app

#### Issue: Handler format wrong
- **Cause:** Vercel Python runtime expects specific format
- **Fix:** Check if handler function signature is correct

### Step 6: Alternative Deployment Options

If Vercel continues to have issues, consider:

1. **Railway** - Better Django support
2. **Render** - Easy Django deployment
3. **Fly.io** - Good for Python apps
4. **Heroku** - Classic option (paid now)

## Next Steps

1. **Check the function logs** (most important!)
2. **Test `/test` endpoint** to verify Python runtime
3. **Share the error message** from logs
4. **Verify all environment variables** are set

The logs will tell us exactly what's wrong!

