from django import forms
from .models import UserProfile, Product, Cart,Supplier  # Ensure Product is imported correctly
from django.contrib.auth.forms import PasswordChangeForm,UserCreationForm
from django.contrib.auth.models import  User

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image','quantity', 'reorderlevel', 'category']
        # fields = '__all__'
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'password', 'confirm_password']
# class UserProfileForm(forms.ModelForm):
#     class Meta:
#         model = UserProfile
#         # fields = ['username', 'email','password'] 
#         fields='__all__'

class UserProfileForm(forms.ModelForm):
   
    class Meta:
        model = UserProfile
        fields = [ 'username','first_name', 'last_name', 'email','profile_picture']
   
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data


class CartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ['user', 'product', 'quantity']

from django.contrib.auth.forms import PasswordChangeForm

class password_changeform(PasswordChangeForm): 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].label = 'Old Password'
        self.fields['new_password1'].label = 'New Password'
        self.fields['new_password2'].label = 'Confirm Password'


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = '__all__'