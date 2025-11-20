# Quick Vercel Deployment Guide

## Step-by-Step Deployment

### 1. Set Environment Variables in Vercel

When you're on the Vercel deployment page (as shown in your screenshot), you need to add environment variables:

**Click on "Environment Variables" section and add:**

```
DATABASE_URL = postgresql://neondb_owner:npg_Xm6ksJTFyIA3@ep-red-pine-ah2qenfa-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
SECRET_KEY = [Generate a random secret key - use: python -c "import secrets; print(secrets.token_urlsafe(50))"]
DEBUG = False
ALLOWED_HOSTS = your-project-name.vercel.app,*.vercel.app
```

### 2. Configure Project Settings

In the Vercel deployment form:

- **Project Name**: `animal-rescue-adoption` (or your preferred name)
- **Framework Preset**: `Other` (as shown in your screenshot)
- **Root Directory**: `./` (default)
- **Build Command**: Leave empty (or use: `pip install -r requirements.txt && python manage.py collectstatic --noinput`)
- **Output Directory**: Leave empty
- **Install Command**: Leave empty (or use: `pip install -r requirements.txt`)

### 3. Deploy

Click the **"Deploy"** button and wait for the build to complete.

### 4. Run Migrations After Deployment

After successful deployment, you need to run migrations. You can do this via:

**Option A: Vercel CLI (Recommended)**
```bash
# Install Vercel CLI
npm i -g vercel

# Login
vercel login

# Link to your project
vercel link

# Run migrations
vercel env pull .env.local
python manage.py migrate
```

**Option B: Direct Database Connection**
```bash
# Set environment variable locally
export DATABASE_URL="postgresql://neondb_owner:npg_Xm6ksJTFyIA3@ep-red-pine-ah2qenfa-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### 5. Create Superuser

After migrations, create an admin account:
```bash
python manage.py createsuperuser
```

## Important Notes

### Environment Variables Required:
- ✅ `DATABASE_URL` - Your Neon PostgreSQL connection string
- ✅ `SECRET_KEY` - Random secret key for Django
- ✅ `DEBUG` - Set to `False` for production
- ✅ `ALLOWED_HOSTS` - Your Vercel domain(s)

### After Deployment:
1. Your app will be live at: `https://your-project-name.vercel.app`
2. Admin panel: `https://your-project-name.vercel.app/admin/`
3. Run migrations before first use
4. Create superuser for admin access

### Troubleshooting:

**If build fails:**
- Check that all environment variables are set
- Verify DATABASE_URL format is correct
- Check build logs in Vercel dashboard

**If database connection fails:**
- Verify DATABASE_URL is correct
- Check Neon database is active
- Ensure SSL mode is set correctly

**If static files don't load:**
- Static files are handled by WhiteNoise
- Check that collectstatic ran during build
- Verify STATIC_ROOT in settings

---

**Your app is ready to deploy!** 🚀

Just add the environment variables in Vercel and click Deploy!

