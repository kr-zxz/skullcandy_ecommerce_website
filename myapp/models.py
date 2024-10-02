from sre_constants import CATEGORY
from django.db import models
from django.contrib.auth.models import AbstractUser,User
from django.shortcuts import render
from django.utils import timezone





class UserProfile(AbstractUser):
    # Add any additional fields you need here
    age = models.PositiveIntegerField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)  # Nullable email field
    
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='user_profiles',  # Custom related name to avoid clashes
        related_query_name='user_profile',
        blank=True,
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='user_profiles',  # Custom related name to avoid clashes
        related_query_name='user_profile',
        blank=True,
        verbose_name='user permissions',
    )

    def __str__(self):
        return self.username

class Category(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='productimages/')
    is_active = models.BooleanField(default=True)
    quantity = models.IntegerField(default=0)
    reorderlevel = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    
   

    def is_at_reorder_level(self):
        return self.quantity == self.reorderlevel

    def __str__(self):
        return self.name
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Cart for {self.user.username}: {self.product.name}"
    

class Order(models.Model):
    STATUS_CHOICES = [
        ('processing', 'Processing'),
        ('out_for_delivery', 'Out for Delivery'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=False)
    fullname = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=10)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='processing')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order for {self.fullname} placed on {self.created_at}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in order {self.order.id}"
# Create your models here.

# supplier.py
class Supplier(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    contact_number = models.CharField(max_length=20)
    email = models.EmailField(max_length=100)
    company_name = models.CharField(max_length=100)
    company_website = models.URLField(max_length=200)
    
    def _str_(self):
        return f"{self.pk} : {self.company_name}"
    


# models.py
class Supplier_order(models.Model):
    STATUS_CHOICES = [
        ('can be satisfied', 'Out for Delivery'),
        ('stock not available', 'Out of stock'),
    ]
    
    supplier_id = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    date_of_order = models.DateField(default=timezone.now)
    delivery_date = models.DateField()
    date_of_delivery = models.DateField(null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='no response')

# models.py

from django.db import models
from django.contrib.auth.models import User

class Doctor(models.Model):
    SPECIALIZATION_CHOICES = [
        ('general', 'General Physician'),
        ('cardiologist', 'Cardiologist'),
        ('dermatologist', 'Dermatologist'),
        # Add other specializations
    ]
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=50, choices=SPECIALIZATION_CHOICES)
    description = models.TextField()
    video_call_link = models.URLField()  # Link for the video call

    def __str__(self):
        return self.name

class DoctorAvailability(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.doctor.name} - {self.date} ({self.start_time} - {self.end_time})"

class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    availability = models.ForeignKey(DoctorAvailability, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default='Pending')
    appointment_time = models.DateTimeField()

    def __str__(self):
        return f"{self.user.username} - {self.doctor.name} - {self.appointment_time}"

from django.db import models
from django.contrib.auth.models import User


#visuals
#visuals
from django.db import models

class PatientData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    date = models.DateField(auto_now_add=True)
    sugar_rate = models.FloatField()
    pressure = models.FloatField()
    disease_affected = models.CharField(max_length=200)
    cholesterol_level = models.FloatField()  # Updated field

    def __str__(self):
        return self.name


class ChatHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message_input = models.TextField()
    bot_response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"{self.user.username} - {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"

