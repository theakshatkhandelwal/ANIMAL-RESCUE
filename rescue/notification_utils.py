"""
Utility functions for sending notifications to NGOs/Shelters
"""
from math import radians, cos, sin, asin, sqrt
from .models import Notification, Shelter, Report, AdoptionRequest


def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    Returns distance in kilometers
    """
    if not all([lat1, lon1, lat2, lon2]):
        return None
    
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    
    # Radius of earth in kilometers
    r = 6371
    
    return c * r


def get_nearby_shelters(latitude, longitude, radius_km=50):
    """
    Get all shelters within a specified radius (in kilometers)
    """
    if not latitude or not longitude:
        return Shelter.objects.none()
    
    nearby_shelters = []
    all_shelters = Shelter.objects.filter(
        latitude__isnull=False,
        longitude__isnull=False
    )
    
    for shelter in all_shelters:
        distance = calculate_distance(
            latitude, longitude,
            float(shelter.latitude), float(shelter.longitude)
        )
        if distance and distance <= radius_km:
            nearby_shelters.append((shelter, distance))
    
    # Sort by distance
    nearby_shelters.sort(key=lambda x: x[1])
    return [shelter for shelter, distance in nearby_shelters]


def notify_nearby_shelters_about_report(report):
    """
    Send notifications to all nearby shelters about a new report
    """
    if not report.latitude or not report.longitude:
        return
    
    nearby_shelters = get_nearby_shelters(
        float(report.latitude),
        float(report.longitude),
        radius_km=50  # 50km radius
    )
    
    for shelter in nearby_shelters:
        distance = calculate_distance(
            float(report.latitude), float(report.longitude),
            float(shelter.latitude), float(shelter.longitude)
        )
        
        title = f"New {report.get_report_type_display()} Report Nearby"
        message = (
            f"A new {report.get_report_type_display().lower()} report has been submitted "
            f"for a {report.get_animal_type_display().lower()} approximately {distance:.1f}km away.\n\n"
            f"Location: {report.location}, {report.city}, {report.state}\n"
            f"Description: {report.description[:200]}...\n\n"
            f"Please check the report details and take appropriate action."
        )
        
        Notification.objects.create(
            notification_type='new_report',
            shelter=shelter,
            report=report,
            title=title,
            message=message
        )


def notify_shelter_about_adoption_request(adoption_request):
    """
    Send notification to shelter about a new adoption request
    """
    if not adoption_request.animal.shelter:
        return
    
    shelter = adoption_request.animal.shelter
    
    title = f"New Adoption Request for {adoption_request.animal.name}"
    message = (
        f"{adoption_request.user.get_full_name() or adoption_request.user.username} "
        f"has submitted an adoption request for {adoption_request.animal.name}.\n\n"
        f"Message from applicant:\n{adoption_request.message}\n\n"
        f"Please review and respond to this request."
    )
    
    Notification.objects.create(
        notification_type='adoption_request',
        shelter=shelter,
        adoption_request=adoption_request,
        title=title,
        message=message
    )


def notify_shelter_about_report_update(update):
    """
    Notify shelter about updates to reports they're following
    """
    if not update.report:
        return
    
    # Notify all shelters that were notified about the original report
    notifications = Notification.objects.filter(
        report=update.report,
        notification_type='new_report'
    )
    
    for notification in notifications:
        # Create update notification
        Notification.objects.create(
            notification_type='report_update',
            shelter=notification.shelter,
            report=update.report,
            title=f"Update on Report: {update.title}",
            message=update.content
        )

