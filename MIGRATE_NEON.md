# How to Run Migrations on Neon PostgreSQL Database

## Step 1: Verify Database Connection

Your Neon connection string:
```
postgresql://neondb_owner:npg_Xm6ksJTFyIA3@ep-red-pine-ah2qenfa-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
```

## Step 2: Run Migrations Locally

### Option A: Using Command Line (Recommended)

1. **Set the DATABASE_URL environment variable:**

   **Windows PowerShell:**
   ```powershell
   $env:DATABASE_URL="postgresql://neondb_owner:npg_Xm6ksJTFyIA3@ep-red-pine-ah2qenfa-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
   ```

   **Windows CMD:**
   ```cmd
   set DATABASE_URL=postgresql://neondb_owner:npg_Xm6ksJTFyIA3@ep-red-pine-ah2qenfa-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
   ```

   **Linux/Mac:**
   ```bash
   export DATABASE_URL="postgresql://neondb_owner:npg_Xm6ksJTFyIA3@ep-red-pine-ah2qenfa-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
   ```

2. **Activate your virtual environment:**
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

3. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

4. **Create superuser (optional but recommended):**
   ```bash
   python manage.py createsuperuser
   ```

### Option B: Using .env file

1. Create a `.env` file in your project root:
   ```
   DATABASE_URL=postgresql://neondb_owner:npg_Xm6ksJTFyIA3@ep-red-pine-ah2qenfa-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
   SECRET_KEY=8y3UjX18Ejly__IAEz4WCkxoWjYTbxRcYPrIsofPvFEWANdRZjIAWqqcMQCxL01ULfI
   DEBUG=False
   ```

2. Run migrations:
   ```bash
   python manage.py migrate
   ```

## Step 3: Verify Tables Were Created

You can check in Neon Dashboard:
1. Go to your Neon project
2. Click on "SQL Editor"
3. Run: `SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';`
4. You should see tables like: `auth_user`, `rescue_animal`, `rescue_report`, etc.

## Step 4: Common Issues

### Issue: "relation does not exist"
- **Solution:** Run migrations: `python manage.py migrate`

### Issue: "connection refused" or "timeout"
- **Solution:** Check if your Neon database allows connections from your IP
- In Neon Dashboard: Settings → Connection → Check "Allow connections from any IP"

### Issue: "SSL connection required"
- **Solution:** Your connection string already includes `sslmode=require`, which is correct

### Issue: "authentication failed"
- **Solution:** Verify your connection string is correct
- Check password in Neon Dashboard: Settings → Connection

## Step 5: After Migrations

Once migrations are complete:
1. Your Vercel deployment should work
2. You can create a superuser to access `/admin/`
3. The app should be fully functional

## Quick Test

After running migrations, test the connection:
```bash
python manage.py dbshell
```

If this works, your database is properly configured!

