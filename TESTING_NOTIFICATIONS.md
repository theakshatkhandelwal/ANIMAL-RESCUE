# Testing Guide: NGO Notification System

## Step-by-Step Testing Instructions

### Prerequisites
- Server is running at http://127.0.0.1:8000
- You'll need at least 2 browser windows/tabs (or use incognito mode)

---

## Test Scenario 1: NGO Receives Report Notifications

### Step 1: Create an NGO/Shelter Account

1. **Open Browser Tab 1** (or use incognito)
2. Go to: http://127.0.0.1:8000/register/
3. Register a new account:
   - Username: `ngotest1`
   - Email: `ngo@test.com`
   - Password: `test123456`
   - First Name: `NGO`
   - Last Name: `Test`
4. After registration, you'll be logged in automatically
5. Go to Dashboard: http://127.0.0.1:8000/dashboard/
6. Click **"Create Shelter Profile"**
7. Fill in shelter details:
   - **Name**: `Happy Paws Shelter`
   - **Address**: `123 Main Street`
   - **City**: `Bangalore`
   - **State**: `Karnataka`
   - **ZIP Code**: `560001`
   - **Phone**: `9876543210`
   - **Email**: `ngo@test.com`
8. Click **"Create Shelter"**
9. ✅ You now have an NGO account!

### Step 2: Create a Regular User Account

1. **Open Browser Tab 2** (or use incognito/private window)
2. Go to: http://127.0.0.1:8000/register/
3. Register a new account:
   - Username: `usertest1`
   - Email: `user@test.com`
   - Password: `test123456`
   - First Name: `Test`
   - Last Name: `User`
4. After registration, you'll be logged in automatically

### Step 3: Report an Animal (as User)

1. In **Tab 2** (User account), go to: http://127.0.0.1:8000/reports/create/
2. Fill in the report form:
   - **Report Type**: `Stray Animal`
   - **Animal Type**: `Dog`
   - **Description**: `Found a stray dog near the park`
   - **Location**: `456 Park Avenue`
   - **City**: `Bangalore`
   - **State**: `Karnataka`
   - **ZIP Code**: `560002` (close to NGO location)
   - **Photo**: (Optional - upload any image)
3. Click **"Submit Report"**
4. ✅ You should see: "Report submitted successfully! Nearby NGOs have been notified."

### Step 4: Check Notifications (as NGO)

1. Switch to **Tab 1** (NGO account)
2. Go to Dashboard: http://127.0.0.1:8000/dashboard/
3. ✅ You should see a **"Notifications"** section at the top
4. ✅ You should see:
   - Notification title: "New Stray Animal Report Nearby"
   - Unread count badge
   - Report details
5. Click **"View All"** to see full notifications page
6. ✅ You should see the full notification with:
   - Report type and animal type
   - Location and distance
   - Description
   - "View Report" button

### Step 5: View Report Details

1. In the notifications page, click **"View Report"**
2. ✅ You should see the full report details
3. You can click **"Add Update"** to post updates about the report

---

## Test Scenario 2: NGO Receives Adoption Request Notifications

### Step 1: Add an Animal (as NGO)

1. In **Tab 1** (NGO account), go to Dashboard
2. Click **"Add New Animal"**
3. Fill in animal details:
   - **Name**: `Buddy`
   - **Animal Type**: `Dog`
   - **Breed**: `Labrador Retriever` (use breed suggestions!)
   - **Age**: `2`
   - **Gender**: `Male`
   - **Color**: `Golden`
   - **Size**: `Large`
   - **Description**: `Friendly and playful dog looking for a home`
   - **Status**: `Available for Adoption`
   - **Photo**: (Optional)
4. Click **"Save"**
5. ✅ Animal is now available for adoption

### Step 2: Request Adoption (as User)

1. Switch to **Tab 2** (User account)
2. Go to: http://127.0.0.1:8000/animals/
3. Find the animal you just added (Buddy)
4. Click **"View Details"**
5. ✅ You should see:
   - Animal details
   - **Shelter/NGO information** (highlighted in green)
   - Contact details of the NGO
6. Click **"Request Adoption"**
7. Fill in the adoption message:
   - **Message**: `I would love to adopt Buddy. I have a big yard and experience with dogs.`
8. Click **"Submit Request"**
9. ✅ You should see: "Adoption request submitted! The shelter has been notified."

### Step 3: Check Adoption Notification (as NGO)

1. Switch to **Tab 1** (NGO account)
2. Go to Dashboard: http://127.0.0.1:8000/dashboard/
3. ✅ You should see a new notification:
   - Title: "New Adoption Request for Buddy"
   - Shows applicant name
   - Shows the message
4. Go to Notifications page: http://127.0.0.1:8000/notifications/
5. ✅ You should see the adoption request notification
6. Click **"Manage Request"**
7. ✅ You can now:
   - **Approve** the request
   - **Reject** the request
8. Click **"Approve Request"**
9. ✅ Animal status changes to "Pending"
10. ✅ User will see the status in their dashboard

---

## Test Scenario 3: Notification Management

### Step 1: View All Notifications

1. In **Tab 1** (NGO account), go to: http://127.0.0.1:8000/notifications/
2. ✅ You should see:
   - All notifications (reports and adoption requests)
   - Unread count at the top
   - Notification type badges
   - Timestamps

### Step 2: Mark Individual Notification as Read

1. Find an unread notification
2. Click **"Mark Read"** button
3. ✅ Notification should change appearance (no longer highlighted)
4. ✅ Unread count should decrease

### Step 3: Mark All as Read

1. Click **"Mark All as Read"** button at the top
2. ✅ All notifications should be marked as read
3. ✅ Unread count should be 0

### Step 4: Check Notification Badge in Navigation

1. Look at the top navigation bar
2. ✅ You should see "Notifications" link
3. ✅ If there are unread notifications, you'll see a red badge with the count
4. Click on "Notifications" to go to notifications page

---

## Test Scenario 4: Multiple NGOs and Distance

### Step 1: Create Another NGO

1. **Open Browser Tab 3** (or use another incognito window)
2. Register: `ngotest2` / `ngo2@test.com`
3. Create shelter:
   - **Name**: `City Animal Rescue`
   - **City**: `Mumbai` (different city - won't get notification)
   - **ZIP**: `400001`

### Step 2: Create Report Near First NGO

1. In **Tab 2** (User), create a report in Bangalore
2. ✅ Only the Bangalore NGO should receive notification
3. ✅ Mumbai NGO should NOT receive notification (too far)

---

## Quick Test Checklist

- [ ] NGO can see notifications in dashboard
- [ ] Notification appears when user reports animal nearby
- [ ] Notification shows distance and location
- [ ] NGO can click to view full report
- [ ] NGO receives adoption request notifications
- [ ] NGO can approve/reject adoption requests
- [ ] Notification badge shows in navigation
- [ ] Can mark notifications as read
- [ ] Can mark all as read
- [ ] Unread count updates correctly
- [ ] Only nearby NGOs receive notifications (within 50km)

---

## Troubleshooting

### No notifications appearing?
1. Check that NGO has valid location (city, state, zip)
2. Check that report has valid location
3. Verify both are in same city/area (within 50km)
4. Check browser console for errors

### Notification badge not showing?
1. Make sure you're logged in as NGO (has shelter profile)
2. Refresh the page
3. Check that there are actually unread notifications

### Distance calculation issues?
- The system uses GPS coordinates
- If addresses aren't geocoded, notifications won't work
- Make sure to use real city names for testing

---

## Admin Panel Testing

You can also check notifications in the admin panel:

1. Go to: http://127.0.0.1:8000/admin/
2. Login with admin credentials:
   - Username: `admin`
   - Password: `admin123`
3. Go to **Rescue** → **Notifications**
4. ✅ You can see all notifications in the system
5. ✅ Filter by type, read status, shelter, etc.

---

**Happy Testing! 🎉**

