from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Shelter(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    website = models.URLField(blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='shelter')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Animal(models.Model):
    ANIMAL_TYPES = [
        ('dog', 'Dog'),
        ('cat', 'Cat'),
        ('bird', 'Bird'),
        ('rabbit', 'Rabbit'),
        ('other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('available', 'Available for Adoption'),
        ('pending', 'Pending Adoption'),
        ('adopted', 'Adopted'),
        ('lost', 'Lost'),
        ('found', 'Found'),
    ]

    name = models.CharField(max_length=100)
    animal_type = models.CharField(max_length=20, choices=ANIMAL_TYPES)
    breed = models.CharField(max_length=100, blank=True)
    age = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(30)], null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female'), ('unknown', 'Unknown')])
    color = models.CharField(max_length=50, blank=True)
    size = models.CharField(max_length=20, choices=[('small', 'Small'), ('medium', 'Medium'), ('large', 'Large')], blank=True)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    photo = models.ImageField(upload_to='animals/', blank=True, null=True)
    shelter = models.ForeignKey(Shelter, on_delete=models.CASCADE, related_name='animals', null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='animals_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.get_animal_type_display()})"

    class Meta:
        ordering = ['-created_at']


class Report(models.Model):
    REPORT_TYPES = [
        ('stray', 'Stray Animal'),
        ('lost', 'Lost Pet'),
        ('found', 'Found Animal'),
    ]

    report_type = models.CharField(max_length=20, choices=REPORT_TYPES)
    animal_type = models.CharField(max_length=20, choices=Animal.ANIMAL_TYPES)
    description = models.TextField()
    location = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    photo = models.ImageField(upload_to='reports/', blank=True, null=True)
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports')
    animal = models.ForeignKey(Animal, on_delete=models.SET_NULL, null=True, blank=True, related_name='reports')
    status = models.CharField(max_length=20, choices=[
        ('open', 'Open'),
        ('investigating', 'Investigating'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ], default='open')
    ai_identified_type = models.CharField(max_length=50, blank=True, null=True)
    ai_confidence = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_report_type_display()} - {self.get_animal_type_display()} at {self.location}"

    class Meta:
        ordering = ['-created_at']


class AdoptionRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
    ]

    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name='adoption_requests')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='adoption_requests')
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.animal.name} ({self.status})"

    class Meta:
        ordering = ['-created_at']
        unique_together = ['animal', 'user']


class Update(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name='updates', null=True, blank=True)
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='updates', null=True, blank=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='updates_created')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']


class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('new_report', 'New Animal Report'),
        ('adoption_request', 'Adoption Request'),
        ('report_update', 'Report Update'),
    ]

    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    shelter = models.ForeignKey(Shelter, on_delete=models.CASCADE, related_name='notifications')
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='notifications', null=True, blank=True)
    adoption_request = models.ForeignKey(AdoptionRequest, on_delete=models.CASCADE, related_name='notifications', null=True, blank=True)
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.shelter.name} - {self.title}"

    class Meta:
        ordering = ['-created_at']


