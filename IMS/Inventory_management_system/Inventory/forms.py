from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Category, Unit, InventoryItem
from django.forms import ModelForm

class UserRegistration(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class InventoryItemForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), initial=0)
    unit = forms.ModelChoiceField(queryset=Unit.objects.all(), initial=0)

    class Meta:
        model = InventoryItem
        fields = ['name', 'quantity', 'category', 'unit', 'code']