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
    first_name = forms.CharField(max_length=30, help_text='Enter your first name.')
    last_name = forms.CharField(max_length=30, help_text='Enter your last name.')

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = '__all__'


#visuals
#visuals for sugar and pressure
from django import forms
from .models import PatientData

class PatientDataForm(forms.ModelForm):
    class Meta:
        model = PatientData
        fields = ['name', 'age', 'gender', 'sugar_rate', 'pressure', 'disease_affected', 'cholesterol_level']


#v1
        from django import forms

class TimelineForm(forms.Form):
    disease_name = forms.CharField(label='Disease Name', max_length=100)
    symptom_start_date = forms.DateField(label='Symptom Start Date', widget=forms.SelectDateWidget)
    diagnosis_date = forms.DateField(label='Diagnosis Date', widget=forms.SelectDateWidget)
    treatment_start_date = forms.DateField(label='Treatment Start Date', widget=forms.SelectDateWidget)


#v2
from django import forms

class OutcomeForm(forms.Form):
    disease_name = forms.CharField(label='Disease', max_length=100)
    age = forms.IntegerField(label='Age')
    gender = forms.ChoiceField(label='Gender', choices=[('M', 'Male'), ('F', 'Female')])
    symptom_severity = forms.IntegerField(label='Symptom Severity', min_value=1, max_value=10)


