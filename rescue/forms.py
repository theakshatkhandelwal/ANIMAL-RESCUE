from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Animal, Report, AdoptionRequest, Shelter, Update


class UserRegistrationForm(UserCreationForm):
    USER_TYPE_CHOICES = [
        ('user', 'Regular User'),
        ('ngo', 'NGO/Shelter'),
    ]
    
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    user_type = forms.ChoiceField(
        choices=USER_TYPE_CHOICES,
        required=True,
        widget=forms.RadioSelect(attrs={'class': 'user-type-radio'}),
        initial='user',
        label='I am registering as:'
    )
    
    # NGO/Shelter fields (shown conditionally)
    shelter_name = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Shelter/NGO Name'}),
        label='Shelter/NGO Name'
    )
    shelter_address = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 2, 'class': 'form-control', 'placeholder': 'Street Address'}),
        label='Address'
    )
    shelter_city = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
        label='City'
    )
    shelter_state = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}),
        label='State'
    )
    shelter_zip_code = forms.CharField(
        max_length=10,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ZIP Code'}),
        label='ZIP Code'
    )
    shelter_phone = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
        label='Phone'
    )
    shelter_website = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Website (optional)'}),
        label='Website (optional)'
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        user_type = cleaned_data.get('user_type')
        
        if user_type == 'ngo':
            # Validate NGO fields
            required_fields = {
                'shelter_name': 'Shelter/NGO Name',
                'shelter_address': 'Address',
                'shelter_city': 'City',
                'shelter_state': 'State',
                'shelter_zip_code': 'ZIP Code',
                'shelter_phone': 'Phone',
            }
            
            for field, label in required_fields.items():
                if not cleaned_data.get(field):
                    self.add_error(field, f'{label} is required for NGO registration.')
        
        return cleaned_data


class AnimalForm(forms.ModelForm):
    class Meta:
        model = Animal
        fields = ['name', 'animal_type', 'breed', 'age', 'gender', 'color', 'size', 'description', 'photo', 'status']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'animal_type': forms.Select(attrs={'class': 'form-control'}),
            'breed': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'color': forms.TextInput(attrs={'class': 'form-control'}),
            'size': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'accept': 'image/*', 'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['report_type', 'animal_type', 'description', 'location', 'city', 'state', 'zip_code', 'photo']
        widgets = {
            'report_type': forms.Select(attrs={'class': 'form-control'}),
            'animal_type': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'accept': 'image/*', 'class': 'form-control'}),
        }


class AdoptionRequestForm(forms.ModelForm):
    class Meta:
        model = AdoptionRequest
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Tell us why you would like to adopt this animal...', 'class': 'form-control'}),
        }


class ShelterForm(forms.ModelForm):
    class Meta:
        model = Shelter
        fields = ['name', 'address', 'city', 'state', 'zip_code', 'phone', 'email', 'website']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
        }


class UpdateForm(forms.ModelForm):
    class Meta:
        model = Update
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }

