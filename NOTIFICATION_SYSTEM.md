# Notification System for Users and NGOs

## Overview
The Animal Rescue & Adoption platform now includes a comprehensive notification system that connects users with NGOs (shelters) for both reporting animals and adoption requests.

## How It Works

### For Regular Users

#### 1. **Reporting Animals**
When a user reports a stray, lost, or found animal:
- The system automatically detects the user's location (or uses provided address)
- Calculates distance to all registered NGOs/shelters within 50km radius
- Sends notifications to all nearby NGOs with:
  - Report type (Stray/Lost/Found)
  - Animal type
  - Location details
  - Distance from NGO
  - Description
  - Photo (if uploaded)

#### 2. **Adopting Pets from NGOs**
- Users can browse animals available for adoption
- Each animal shows which NGO/shelter it belongs to
- Users can submit adoption requests directly
- NGOs receive instant notifications about adoption requests
- NGOs can approve or reject requests from their dashboard

### For NGOs/Shelters

#### 1. **Receiving Notifications**
NGOs receive notifications for:
- **New Reports**: When users report animals within 50km radius
  - Includes location, distance, animal type, and description
  - Direct link to view full report details
  - Option to add updates to the report

- **Adoption Requests**: When users want to adopt their animals
  - Applicant details and message
  - Direct link to manage the request
  - Can approve or reject from dashboard

- **Report Updates**: When updates are posted on reports they're following

#### 2. **Notification Management**
- **Dashboard**: Shows recent notifications with unread count
- **Notifications Page**: Full list of all notifications
- **Mark as Read**: Individual or bulk mark as read
- **Quick Actions**: Direct links to view reports, manage adoptions, etc.

#### 3. **Managing Animals**
- Add animals available for adoption
- View adoption requests for each animal
- Approve/reject adoption requests
- Update animal status (Available → Pending → Adopted)

## Features

### Location-Based Matching
- Uses GPS coordinates to find nearby NGOs
- Calculates distance using Haversine formula
- Default radius: 50 kilometers (configurable)
- Only notifies NGOs with valid location data

### Real-Time Notifications
- Instant notifications when reports are created
- Instant notifications for adoption requests
- Notification badge in navigation bar
- Unread count displayed prominently

### User Experience
- **For Users**: Simple reporting and adoption process
- **For NGOs**: Centralized dashboard to manage all activities
- Clear visual indicators for unread notifications
- Easy navigation to related content

## Technical Details

### Notification Types
1. **new_report**: New animal report nearby
2. **adoption_request**: New adoption request for NGO's animal
3. **report_update**: Update posted on a report

### Distance Calculation
- Uses Haversine formula for accurate distance calculation
- Considers Earth's curvature
- Returns distance in kilometers

### Database Models
- **Notification**: Stores all notifications with read/unread status
- Links to Report, AdoptionRequest, and Shelter
- Timestamped for chronological ordering

## Workflow Examples

### Example 1: User Reports Stray Dog
1. User fills out report form with location
2. System geocodes the address
3. Finds all NGOs within 50km
4. Creates notification for each nearby NGO
5. NGOs see notification in dashboard
6. NGO clicks to view full report
7. NGO can add updates or take action

### Example 2: User Wants to Adopt
1. User browses available animals
2. Finds a dog from "Happy Paws Shelter"
3. Clicks "Request Adoption"
4. Fills out adoption message
5. System creates adoption request
6. "Happy Paws Shelter" receives notification
7. NGO reviews request in dashboard
8. NGO approves/rejects request
9. User receives status update

## Benefits

### For Users
- Easy reporting process
- Automatic connection to nearby NGOs
- Clear adoption process
- Direct communication with shelters

### For NGOs
- Never miss a nearby report
- Centralized management
- Quick response to adoption requests
- Better coordination with community

## Future Enhancements
- Email notifications (optional)
- SMS notifications for urgent cases
- Customizable notification radius per NGO
- Notification preferences (types to receive)
- Push notifications for mobile apps

---

**The system is now live and ready to connect users with NGOs!** 🎉

