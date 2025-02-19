from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Category, Unit, InventoryItem
from django.forms import ModelForm, formset_factory

class UserRegistration(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class InventoryItemForm(forms.ModelForm):
    class Meta:
        model = InventoryItem
        fields = ['name', 'quantity', 'category', 'unit', 'code']

# Create a formset that allows an unlimited number of forms
InventoryItemFormSet = formset_factory(InventoryItemForm, extra=1, can_delete=True)