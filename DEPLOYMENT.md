# Deployment Guide

## Deploying to Vercel with Neon PostgreSQL

### Prerequisites
- GitHub repository connected
- Neon PostgreSQL database (connection string provided)
- Vercel account

### Step 1: Set Environment Variables in Vercel

When deploying on Vercel, add these environment variables:

1. Go to your Vercel project settings
2. Navigate to **Environment Variables**
3. Add the following:

```
DATABASE_URL=postgresql://neondb_owner:npg_Xm6ksJTFyIA3@ep-red-pine-ah2qenfa-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
SECRET_KEY=your-secret-key-here-change-this-to-random-string
DEBUG=False
ALLOWED_HOSTS=your-vercel-domain.vercel.app,*.vercel.app
```

### Step 2: Deploy on Vercel

1. **Import from GitHub:**
   - Go to Vercel Dashboard
   - Click "Add New Project"
   - Import from GitHub: `theakshatkhandelwal/ANIMAL-RESCUE`
   - Select the repository

2. **Configure Project:**
   - **Framework Preset**: Other
   - **Root Directory**: `./` (default)
   - **Build Command**: Leave empty (Vercel will auto-detect)
   - **Output Directory**: Leave empty

3. **Environment Variables:**
   - Add `DATABASE_URL` with your Neon PostgreSQL connection string
   - Add `SECRET_KEY` (generate a random string)
   - Add `DEBUG=False`
   - Add `ALLOWED_HOSTS=your-domain.vercel.app,*.vercel.app`

4. **Deploy:**
   - Click "Deploy"
   - Wait for build to complete

### Step 3: Run Migrations

After deployment, you need to run migrations on the production database:

**Option 1: Using Vercel CLI**
```bash
vercel env pull .env.local
python manage.py migrate
```

**Option 2: Using Vercel Functions**
Create a one-time migration script or use Vercel's CLI to run commands.

**Option 3: Direct Database Access**
You can also run migrations locally pointing to the production database:
```bash
export DATABASE_URL="your-neon-connection-string"
python manage.py migrate
```

### Step 4: Create Superuser

```bash
export DATABASE_URL="your-neon-connection-string"
python manage.py createsuperuser
```

### Step 5: Collect Static Files

Static files should be collected automatically during build, but if needed:
```bash
python manage.py collectstatic --noinput
```

## Alternative: Deploy to Other Platforms

### Heroku

1. Install Heroku CLI
2. Login: `heroku login`
3. Create app: `heroku create your-app-name`
4. Set environment variables:
   ```bash
   heroku config:set DATABASE_URL="your-neon-connection-string"
   heroku config:set SECRET_KEY="your-secret-key"
   heroku config:set DEBUG=False
   ```
5. Deploy: `git push heroku main`
6. Run migrations: `heroku run python manage.py migrate`
7. Create superuser: `heroku run python manage.py createsuperuser`

### Railway

1. Connect GitHub repository
2. Add PostgreSQL service (or use external Neon DB)
3. Set environment variables
4. Deploy automatically

### Render

1. Create new Web Service
2. Connect GitHub repository
3. Set build command: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
4. Set start command: `gunicorn animal_rescue.wsgi:application`
5. Add environment variables
6. Deploy

## Important Notes

### Static Files
- WhiteNoise is configured for serving static files
- Static files are collected during build
- Media files may need cloud storage (AWS S3, Cloudinary) for production

### Database
- Using Neon PostgreSQL (provided connection string)
- SSL mode is required
- Connection pooling is enabled

### Security
- Set `DEBUG=False` in production
- Use strong `SECRET_KEY`
- Configure `ALLOWED_HOSTS` properly
- Use environment variables for sensitive data

## Troubleshooting

### Database Connection Issues
- Verify DATABASE_URL is set correctly
- Check SSL mode requirements
- Ensure database is accessible from deployment platform

### Static Files Not Loading
- Run `collectstatic` during build
- Check WhiteNoise configuration
- Verify STATIC_ROOT path

### Migration Issues
- Run migrations after deployment
- Check database permissions
- Verify connection string format

---

**Ready to deploy!** 🚀

