# 🔗 How to Change Your Render URL

## Current URL
`https://animal-rescue-fndp.onrender.com`

## Change Service Name

1. **Go to Render Dashboard** → Your Web Service
2. Click **"Settings"** tab (left sidebar)
3. Find **"Name"** field at the top
4. Change it to your desired name (e.g., `animal-rescue` or `my-animal-app`)
5. Click **"Save Changes"**
6. Render will automatically update the URL

## New URL Format

After changing the name, your new URL will be:
```
https://your-new-name.onrender.com
```

## Important Notes

1. **URL Availability**: The name must be unique across all Render services
2. **Update ALLOWED_HOSTS**: If you set a specific domain, update the `ALLOWED_HOSTS` environment variable
3. **Custom Domain**: You can also add a custom domain in Settings → Custom Domain

## Example

If you change the name to `animal-rescue`:
- New URL: `https://animal-rescue.onrender.com`
- Update `ALLOWED_HOSTS` to: `animal-rescue.onrender.com,*.onrender.com` (or just `*`)

## After Changing

1. Wait a few minutes for DNS to update
2. Your old URL will redirect to the new one
3. Update any bookmarks or links you've shared

---

**That's it! Just change the service name in Settings.** ✅


