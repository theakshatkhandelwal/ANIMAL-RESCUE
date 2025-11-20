# Registration Update: User Type Selection

## What Changed

The registration form now includes a **User Type Selection** that makes it easy to register as either:
- **Regular User** - For individuals who want to report animals or adopt pets
- **NGO/Shelter** - For organizations that manage animals and receive notifications

## New Registration Flow

### For Regular Users:
1. Go to Register page
2. Select **"Regular User"** option
3. Fill in basic information (username, name, email, password)
4. Submit → Account created, redirected to home page

### For NGOs/Shelters:
1. Go to Register page
2. Select **"NGO/Shelter"** option
3. Fill in basic information (username, name, email, password)
4. **Additional NGO fields appear automatically:**
   - Shelter/NGO Name *
   - Address *
   - City *
   - State *
   - ZIP Code *
   - Phone *
   - Website (optional)
5. Submit → Account created + Shelter profile created automatically
6. Redirected to Dashboard (already set up as NGO)

## Features

### Visual Design
- **Radio button selection** with icons (👤 User / 🏢 NGO)
- **Interactive selection** - highlights when selected
- **Conditional fields** - NGO fields only appear when "NGO/Shelter" is selected
- **Clear visual separation** - NGO section has distinct styling

### Validation
- NGO fields are **required** when NGO is selected
- Form validates all required fields before submission
- Clear error messages for missing fields

### Automatic Setup
- When NGO is selected, shelter profile is **automatically created**
- Location is **automatically geocoded** (latitude/longitude)
- NGO can immediately start using the platform
- No need to create shelter profile separately

## Benefits

### For Users:
- ✅ Simpler registration process
- ✅ Clear distinction between user types
- ✅ No confusion about what to select

### For NGOs:
- ✅ One-step registration (no separate shelter creation)
- ✅ Immediate access to NGO features
- ✅ Automatic location setup for notifications
- ✅ Ready to receive notifications right away

## Technical Details

### Form Fields:
- `user_type`: Radio selection (user/ngo)
- Conditional NGO fields shown/hidden via JavaScript
- Validation ensures NGO fields are filled when NGO is selected

### Backend Processing:
- Creates User account
- If NGO selected: Creates Shelter profile automatically
- Geocodes address for location-based notifications
- Redirects to appropriate page (home for users, dashboard for NGOs)

## Testing

### Test Regular User Registration:
1. Go to `/register/`
2. Select "Regular User"
3. Fill form (no NGO fields should appear)
4. Submit → Should redirect to home page

### Test NGO Registration:
1. Go to `/register/`
2. Select "NGO/Shelter"
3. NGO fields should appear automatically
4. Fill all fields including NGO information
5. Submit → Should redirect to dashboard
6. Check dashboard → Should see NGO features (notifications, add animals, etc.)

---

**The registration process is now much simpler and more intuitive!** 🎉

