from turtle import home
from django.shortcuts import render,redirect
from django.urls import path, include
from . import views
from .views import *
from .views import index, user_register, admin_login, search, user_login, admin_add, adminpage, edit_product, delete_product, add_to_cart, decrease_to_cart, cart, checkout_view
from django.contrib.auth import views as auth_views
from .views import product_list
from .views import medical_advisor_view, medical_advisor_result_view  # Make sure this is imported

urlpatterns = [
    path('admin_login/', views.admin_login, name='admin_login'),
    path('search/', views.search_view, name='search'),
    path('user_login/', views.user_login, name='user_login'),
    path('user/register/', views.user_register, name='user_register'),
    path('user_logout/', views.user_logout, name='user_logout'),
    path('register/', user_register, name='user_register'),
    path('accounts/', include("django.contrib.auth.urls")),
    path('admin_add/', views.admin_add, name='admin_add'),
    path('adminpage', views.adminpage, name='adminpage'),
    path('reoder/', views.reoder, name='reoder'),
    path('adminpageorder/', views.admin_order_view, name='adminorders'),
    path('adminordersiteam/<int:order_id>/', views.order_detail_view, name='order_detail'),
    path('userpageorder/', views.user_order_view, name='orders'),
    path('index/', views.index, name='index'),
    path('edit_product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('add_to_wishlist/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove_to_wishlist/<int:product_id>/', views.remove_to_wishlist, name='remove_to_wishlist'),
    path('dec_from_cart/<int:product_id>/', views.decrease_to_cart, name='decrease_quantity'),
    path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/', views.cart, name='cart'),
    path('view_to_wishlist/', views.view_to_wishlist, name='view_to_wishlist'),
    path('checkout/', views.checkout_view, name='checkout'),  
    path('order_summary/', views.order_summary_view, name='order_summary'),  
    # path('profile/update/', views.profile_update, name='profile_update'),
    path('accounts/', include('django.contrib.auth.urls')),  # Include Django's authentication URLs
    path('profile/update/', views.profile_update, name='profile_update'),
    path('update_status/<int:order_id>/', views.update_status, name='update_status'),
    path('order_list_and_detail/', views.order_list_and_detail, name='order_list_and_detail'),
    path('products/', products, name='products'),  
    path('home', home, name='home'),

    
     path('prod/', product_list, name='product_list'),
     path('supplier_add/',views.supplier_add,name='supplier_add'),
     path('send_request/<int:product_id>/', views.send_request, name='send_request'),
     path('supplier/<int:id>',views.supplier_replay,name="supplier_replay"),
     path('supplier_replies/', views.supplier_replies, name='supplier_replies'),  # New URL pattern for supplier replies
     path('', views.welcome, name='welcome'),
     #doctors
     path('doctors/', views.doctor_list, name='doctor_list'),
     path('doctors/<int:doctor_id>/', views.doctor_availability, name='doctor_availability'),
     path('book/<int:availability_id>/', views.book_appointment, name='book_appointment'),
     path('appointment/success/', views.appointment_success, name='appointment_success'),
     path('cancel-appointment/<int:appointment_id>/', views.cancel_appointment, name='cancel_appointment'),
     path('reschedule-appointment/<int:appointment_id>/', views.reschedule_appointment, name='reschedule_appointment'),
     #dashboard
     path('medical-advisor/', medical_advisor_view, name='medical_advisor'),
     path('advice-results/', advice_results_view, name='advice_results'),
     path('visuals/',views.visuals, name='visuals'),


    path('admin/appointments/', views.admin_appointment_list, name='admin_appointment_list'),
    path('admin/appointments/approve/<int:appointment_id>/', views.approve_appointment, name='approve_appointment'),
     
     #visuals
     
     #views for visuals sugar and pressure
     path('form/', views.patient_form, name='patient_form'),
     path('data/', views.patient_data, name='patient_data'),
     path('download/csv/', views.download_csv, name='download_csv'),
     path('download/pdf/', views.download_pdf, name='download_pdf'),

     #v1
    path('timelin/', views.timeline_view, name='timeline'),
    path('outcome-comparison/', views.outcome_view, name='outcome_comparison'),

    path('chat_home/', views.chat_home, name='chat_home'),
    
    path('patient-data/', patient_data_visualization, name='patient_data_visualization'),
    path('my-appointments/', views.user_appointment_list, name='user_appointment_list'),
    path('cancel-appointment/<int:appointment_id>/', views.cancel_appointment, name='cancel_appointment'),

    

   
        path('visualizations/', visualizations, name='visualizations'),

     


     

    
     

]

   
    

