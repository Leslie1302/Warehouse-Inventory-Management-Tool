from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Category, Unit, InventoryItem, MaterialOrder, Profile
from django.forms import ModelForm, formset_factory, modelformset_factory

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


class MaterialOrderForm(forms.ModelForm):
    class Meta:
        model = MaterialOrder
        fields = ['name', 'quantity', 'category', 'code', 'unit']
        widgets = {
            'name': forms.Select(attrs={'class': 'form-control material-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control material-code', 'readonly': 'readonly'}),
            'unit': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].queryset = InventoryItem.objects.all()
        self.fields['name'].empty_label = "-- Choose Material --"

# Create a formset for multiple requests
MaterialOrderFormSet = modelformset_factory(
    MaterialOrder, form=MaterialOrderForm, extra=1, can_delete=True
)





class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture']

class PasswordChangeForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput)
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password != confirm_password:
            raise forms.ValidationError("New passwords do not match.")
        return cleaned_data

class ExcelUploadForm(forms.Form):
    file = forms.FileField()