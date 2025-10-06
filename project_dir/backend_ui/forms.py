from django import forms
from .models import *

class HotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = '__all__'

class RoomForm(forms.ModelForm):
    hotel = forms.ModelChoiceField(
        queryset=Hotel.objects.all(),
        empty_label="Select a Hotel",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Room
        fields = '__all__'

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = '__all__'

class StaffForm(forms.ModelForm):
    hotel = forms.ModelChoiceField(
        queryset=Hotel.objects.all(),
        empty_label="Select a Hotel",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    class Meta:
        model = Staff
        fields = ['hotel', 'name', 'position', 'salary']