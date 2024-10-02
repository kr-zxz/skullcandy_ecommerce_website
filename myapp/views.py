import os
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from .forms import ProductForm
from .models import Category, ChatHistory, Product, UserProfile,Supplier,Supplier_order
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm
from django.shortcuts import render, redirect
from .models import UserProfile,Order,OrderItem
from .forms import CustomUserCreationForm,SupplierForm
from django.db.models import F
from django.conf import settings
from django.core.mail import send_mail


def send_mail_from_website(subject,message,email):
    subject = subject
    message = message
    from_email = settings.EMAIL_HOST_USER
    to_email = [email]
    print(from_email,'to',to_email)


    send_mail(subject, message, from_email, to_email)

def adminpage(request):
    products_at_reorder_level = Product.objects.filter(quantity__lte=F('reorderlevel'))
    products = Product.objects.all()

    context = {
        'products_at_reorder_level': products_at_reorder_level,
        'productdata': products
    }
    
    return render(request, 'user.html', context)

def reoder(request):
    products_at_reorder_level = Product.objects.filter(quantity__lte=F('reorderlevel'))
    
    context = {
        'products_at_reorder_level': products_at_reorder_level,
    
    }
    
    return render(request, 'relevelorder.html', context)


def admin_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_superuser:
                login(request, user)
                url='/adminpage'
                x=f'''
                    <script>
                        alert("wlecome admin");
                        window.location.href = "{url}"; 
                    </script>
                '''
                
                return HttpResponse(x)
        else:
            form = AuthenticationForm()  
            error_message = 'Invalid credentials. Please try again.'
            return render(request, 'admin_login.html', {'form': form, 'error_message': error_message})
    
    else:
        form = AuthenticationForm()

    return render(request, 'admin_login.html', {'form': form})


def user_register(request):
    registration_successful = False

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user to the database
            login(request, user)  # Log the user in
            registration_successful = True
            return redirect('user_login')  # Redirect to the login page
    else:
        form = CustomUserCreationForm()  # Create an empty form

    return render(request, 'user_register.html', {'form': form, 'registration_successful': registration_successful})

    return render(request, 'user_register.html', {'form': form, 'registration_successful': registration_successful})
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm

# def user_login(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(request, data=request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             user = authenticate(request, username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect('medical-advisor')
#             else:
#                 form.add_error(None, 'Invalid username or password')
#         else:
#             # Clear the password field for security reasons
#             form.data = form.data.copy()
#             form.data['password'] = ''
#     else:
#         form = AuthenticationForm()
    
#     return render(request, 'user_login.html', {'form': form})




def user_logout(request):
    logout(request)
    # Redirect to the index page after logout

    return redirect('welcome')


from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_superuser:
                    return redirect('adminpage')  # Redirect admin to admin page
                else:
                    return redirect('welcome')  # Redirect regular user to index page
            else:
                error_message = 'Invalid credentials. Please try again.'
                return render(request, 'user_login.html', {'form': form, 'error_message': error_message})
    else:
        form = AuthenticationForm()
    
    return render(request, 'user_login.html', {'form': form})



from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from .forms import password_changeform

@login_required
def profile_update(request):
    print(request.user)

    if request.method == 'POST':
        print(request.user)
        password_form = password_changeform(request.user,request.POST ,)
        print('kkko',password_form)

        if password_form.is_valid() :
            user = password_form.save()
            update_session_auth_hash(request,user)
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('user_login')  # Redirect to the profile update page
    else:
        password_form = password_changeform(request.user)
    return render(request, 'profile_update.html', {'password_form': password_form})

#122222@@@AA

def admin_add(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        print(form)
        if form.is_valid():
            # # Get the form data including quantity and reorderlevel
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            price = form.cleaned_data['price']
            image = form.cleaned_data['image']
            quantity = form.cleaned_data['quantity']
            reorderlevel = form.cleaned_data['reorderlevel']
            category = form.cleaned_data['category']


            # Create a new product instance
            new_product = Product.objects.create(
                name=name,
                description=description,
                price=price,
                image=image,
                quantity=quantity,
                reorderlevel=reorderlevel,
                category=category
            )
            # Save the new product to the database
            new_product.save()
            

            return redirect('adminpage')  # Redirect after adding a product
        else:
            print(form)
    else:
        form = ProductForm()

    return render(request, 'admin_add.html', {'form': form})

def index(request):   #user page product view
    products = Product.objects.all()
    return render(request, 'index.html', {'productdata': products})

from django.urls import reverse



def product_list(request): #admin page product view
    products = Product.objects.all()
    return render(request, 'myapp/user.html', {'product': products})


def edit_product(request, product_id):
    product_to_edit = get_object_or_404(Product, pk=product_id)
    form = ProductForm(request.POST, request.FILES, instance=product_to_edit)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
        # product_to_edit.name = request.POST.get('name')
        # product_to_edit.description = request.POST.get('description')
        # product_to_edit.price = request.POST.get('price')
        # product_to_edit.quantity = request.POST.get('quantity')
        # product_to_edit.save()
        return redirect('adminpage')  # Redirect to the user page
    else:
        form = ProductForm(instance=product_to_edit)

    return render(request, 'edit_product.html', {'form': form, 'product': product_to_edit})



def delete_product(request, product_id):
    product_to_delete = get_object_or_404(Product, pk=product_id)  # Assuming product is the name of model

    if request.method == 'POST':
        confirmation = request.POST.get('confirmation', None)
        if confirmation == 'confirmed':
            #product_to_delete.is_active = False  # Set the product as inactive
            product_to_delete.delete()
            return redirect('adminpage')  # Redirect to the user page after deletion
        else:
            return redirect('adminpage')  # Redirect without deleting if not confirmed

    return render(request, 'confirmation_page.html', {'product': product_to_delete})
    


def search(request):
    query = request.GET.get('query')
    products = Product.objects.filter(name__icontains=query, is_active=True)
    return render(request, 'search_results.html', {'products': products, 'query': query})

def search_view(request):
    query = request.GET.get('query', '')

    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = []

    context = {
        'query': query,
        'products': products,
    }

    return render(request, 'search_results.html', context)

# from requests import request






def checkout_view(request):
    cart_iteam=Cart.objects.filter(user=request.user)
    print(cart_iteam)
    total_amount=0
    for iteam in cart_iteam:
        total_amount+=iteam.quantity*iteam.product.price

    if request.method == 'POST':
        # Retrieve form data
        fullname = request.POST.get('Fullname')
        address = request.POST.get('address')
        city = request.POST.get('city')
        postal_code = request.POST.get('postal_code')

        # Construct redirect URL with parameters
        redirect_url = reverse('order_summary')
        params = {
            'fullname': fullname,
            'address': address,
            'city': city,
            'postal_code': postal_code,
            'total_amount': total_amount,
        }

        redirect_url += '?' + '&'.join([f"{key}={value}" for key, value in params.items()])
        return HttpResponse(pop_message(redirect_url,'checkout done'))
        
    return render(request, 'checkout.html', {'total_amount': total_amount})

def order_summary_view(request):
    fullname = request.GET.get('fullname')
    address = request.GET.get('address')
    city = request.GET.get('city')
    postal_code = request.GET.get('postal_code')
    total_amount = request.GET.get('total_amount')
    print('asas')
    cart_product = Cart.objects.filter(user=request.user)

    print(cart_product)
    
    # product_ids = list(cart.keys())
    # qu=list(cart.values())
    
    # print(product_ids,qu)
    
    # cart_products = []

    # if product_ids:
    #     final=[]
    #     cart_products = Product.objects.filter(id__in=product_ids)
    #     for i,j in zip(cart_products,qu):
    #         print(i.name,j)
    #         final.append({'name':i.name,'quanity':j})

    print(cart_product)
    context = {
        'fullname': fullname,
        'address': address,
        'city': city,
        'postal_code': postal_code,
        'total_amount': total_amount,
        'cart_products': cart_product
        
    }

    order = Order.objects.create(
                user=request.user,
                fullname=fullname,
                address=address,
                city=city,
                postal_code=postal_code,
                total_amount=total_amount,
            )
            
            # Retrieve and clear cart items for the current user
    cart_items = Cart.objects.filter(user=request.user)
    for cart_item in cart_items:
        order.items.create(product=cart_item.product, quantity=cart_item.quantity)
    
    # cwhart_item.delete()
            
    


    
    return render(request, 'order_summary.html', context)


from .models import Cart
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required(login_url=user_login)
def add_to_cart(request, product_id):

    product = Product.objects.get(pk=product_id)
    # print(isinstance(request.user,UserProfile)
    if request.method=='POST':
        if product.quantity > 0:
            cart_item = Cart(user=request.user, product=product, quantity=1)  # Adjust quantity as needed
            cart_item.save()
            # Decrease product quantity by 1
            product.quantity -= 1
            product.save()
            # Redirect to the cart page or product detail page
            return redirect('cart')  # Redirect to cart page or wherever you manage cart items
        else:
            # Handle out of stock case
            return render(request, 'out_of_stock.html', {'product': product})
        
    else:
        return redirect('product_detail', product_id=product_id)

def decrease_to_cart(request, product_id):
    cart_items = Cart.objects.filter(product_id=product_id,user=request.user).first()
    print('============')
    print("items",cart_items)

    cart_items.delete()
    return redirect('cart')




def remove_from_cart(request, product_id):
    print('--------')
    cart_items = Cart.objects.filter(product_id=product_id,user=request.user).all()
    print('============')
    print("items",cart_items)
    cart_items.delete()
    return redirect('cart')



# def cart(request):
#     cart = request.session.get('cart', {})
#     product_ids = list(cart.keys())

#     cart_items = []
#     total_amount = 0

#     if product_ids:
#         cart_products = Product.objects.filter(id__in=product_ids)
#         for cart_product in cart_products:
#             quantity = cart.get(str(cart_product.id), 0)
#             if quantity > 0:
#                 item_total = quantity * cart_product.price
#                 total_amount += item_total
#                 cart_items.append({
#                     'product': cart_product,
#                     'quantity': quantity,
#                     'item_total': item_total,
#                 })
    

#     return render(request, 'cart.html', {'cart_products': cart_items, 'total_amount': total_amount})

from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart, Product
@login_required(login_url=user_login)
def cart(request):
    upcart_items = Cart.objects.filter(user=request.user)
    
    
    # <QuerySet [<Cart: Cart for alvin: Apple VX max>, <Cart: Cart for alvin: Apple VX max>]>
    cart_items={}
    for item in upcart_items:
        # print(item.product.name)
        
        if item.product.name in cart_items:
            cart_items[item.product.name]['quantity']+=1
            cart_items[item.product.name]['total_price']+=cart_items[item.product.name]['price']
            
        else:
            cart_items[item.product.name]={
                'id':item.product.id,
                'name':item.product.name,
                'price':item.product.price,
                'quantity':item.quantity,
                'price':item.product.price,
                'total_price':item.product.price,
                'image':item.product.image
            }
            # print(cart_items)

    total_price = sum(item['total_price'] for item in cart_items.values())

    
    context= {
        'cart_items': cart_items,
        'total_price': total_price
        }
    
    return render(request, 'cart.html',context)
 
def product_detail(request, product_id):
    product = Product.objects.get(pk=product_id)
    if request.method == 'POST':
        # Handle adding product to cart
        if product.quantity > 0:
            # Decrement quantity and add to cart logic here
            product.quantity -= 1
            product.save()
            # Add to cart logic here
            return redirect('cart')  # Redirect to cart page after adding to cart
        else:
            # Product is out of stock, handle this case as needed
            return render(request, 'product_detail.html', {'product': product, 'message': 'Out of Stock'})
    else:
        return render(request, 'product_detail.html', {'product': product})
#wishlist
@login_required(login_url=user_login)
def add_to_wishlist(request, product_id):
    if 'wishlist' not in request.session:  
        request.session['wishlist'] = []  

    wishlist = request.session['wishlist'] 
    if product_id not in wishlist:  
        wishlist.append(product_id)
        request.session['wishlist'] = wishlist 
        message='Item added to your wishlist!'
    else:
        message='Item already in wishlist'

    url='/'
    return HttpResponse(pop_message(url,message))
#return HttpRespone
    
@login_required(login_url=user_login)
def remove_to_wishlist(request, product_id):
    wishlist = request.session['wishlist']   
    wishlist.remove(product_id)
    request.session['wishlist']=wishlist
    return redirect('index')





@login_required(login_url=user_login)
def view_to_wishlist(request):
    if 'wishlist' not in request.session:  
        context={
            'product':'',
        }
    else:
        wishlist = request.session['wishlist'] 
        data=Product.objects.filter(id__in=wishlist)
        
        context={
            'data':data
        }

    return render(request,'wishlist.html',context)



#custom popup message

def pop_message(url,message):
    url=url
    x=f'''
        <script>
            alert("{message}");
            window.location.href = "{url}"; 
        </script>
    '''
    return(x)



@login_required
def admin_order_view(request):
    # Admin view to display all orders
    orders = Order.objects.all()

    context = {'orders': orders}

    return render(request, 'order_list_and_detail.html', context)

@login_required
def order_detail_view(request, order_id):
    # Admin view to display order details

    order = Order.objects.get(id=order_id)
    get_image=OrderItem.objects.filter(order=order_id)[:1]#just want to call one element
    for i in get_image:
        get_image=i.product.image
        break
    print(get_image)

    items = order.items.all()
    product_count={}
    for item in items:
        if item.product in product_count.keys():
            product_count[item.product] += 1
        else:
            product_count[item.product] = 1
    

    context = {
                'order': order,
                'get_image':get_image,
                'product_count': product_count}
    return render(request, 'order_detail.html', context)

@login_required
def update_status(request, order_id):
    # Update order status view
    if request.method == 'POST':
        new_status = request.POST.get('status')
        try:
            order = Order.objects.get(pk=order_id)
            order.status = new_status
            order.save()
            messages.success(request, 'Order status updated successfully.')
        except Order.DoesNotExist:
            messages.error(request, 'Order not found.')
    return redirect('order_list_and_detail')  # Redirect to orders list
def order_list_and_detail(request):
    if request.user.is_superuser:
        orders = Order.objects.filter()
    else:
        orders = Order.objects.filter(user=request.user)
    context = {'orders': orders}
    return render(request, 'order_list_and_detail.html', context)

from django.contrib.auth.decorators import login_required
from .models import Order

@login_required
def user_order_view(request):
    # Fetch orders associated with the logged-in user
    orders = Order.objects.filter(user=request.user)
    context = {'orders': orders}
    return render(request, 'order_list_and_detail.html', context)


def product_list(request, category_id=None):
    category = Category.objects.get(pk=category_id) if category_id else None
    if category:
        subcategories = category.children.all()
        products = Product.objects.filter(category=category)
    else:
        products = Product.objects.all()
        subcategories = None
    return render(request, 'product_list.html', {'products': products, 'subcategories': subcategories})


from django.shortcuts import render
from .models import Category

def admin_add_product(request):
    categories = Category.objects.all()  # Fetch all categories from the database
    return render(request, 'admin_add_product.html', {'categories': categories})


from django.shortcuts import render
from .models import Product, Category

# def home(request):
#     categories = Category.objects.all()
#     selected_category = None
#     products = Product.objects.all()

#     if 'category' in request.GET:
#         category_id = request.GET['category']
#         if category_id:
#             selected_category = Category.objects.get(pk=category_id)
#             products = Product.objects.filter(category=selected_category)

#     context = {
#         'categories': categories,
#         'selected_category': selected_category,
#         'products': products,
#     }
#     return render(request, 'home.html', context)

from django.shortcuts import render

# Define the home view with request as an argument
def home(request):
    return render(request, 'home.html')  # Render the template for home page

from django.shortcuts import render
from django.db.models import Count
from .models import Product

def products(request):
    # Get all unique categories along with their counts
    categories = Product.objects.values('category').annotate(count=Count('category'))
    
    # Check if category filter is applied
    category = request.GET.get('category')
    if category:
        products = Product.objects.filter(category=category)
    else:
        products = Product.objects.all()
    
    return render(request, 'products.html', {'productdata': products, 'categories': categories})

def supplier_add(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('adminpage')
    else:
        form = SupplierForm()
        print(form)

    context={
        'form':form


    }
    return render(request,'supplier_add.html',context)

def send_request(request,product_id):
    print(product_id)
    if request.method=='POST':
        selected_supplier=request.POST.get('supplier')
        quantity_needed=request.POST.get('quantity')
        date_of_delivery=request.POST.get('DATE')
        stock=Product.objects.get(id=product_id)
        supplier_detail=Supplier.objects.get(id=selected_supplier)
        subject ='REQUEST OF PRODUCT FROM SKULLCANDY'
        St=Supplier_order(
            supplier_id = supplier_detail,
            product_id = stock,
            quantity = quantity_needed,
            delivery_date = date_of_delivery
            

        )
        St.save()
        print(St.id)

        message = f'''
Dear {supplier_detail.name},

We request you to supply the products mentioned below:

<table>
    <tr>
        <th>Product Name</th>
        <th>Quantity</th>
        <th>Date of Delivery</th>
    </tr>
    <tr>
        <td>{stock.name}</td>
        <td>{quantity_needed}</td>
        <td>{date_of_delivery}</td>
    </tr>
</table>

Click the link below to reorder:

[Insert link here]

Best regards,
Roboindia Team
''' 
        message = f'''
Dear {supplier_detail.name},

We request you to supply the products mentioned below:

        Product Name:{stock.name}
        Quantity:{quantity_needed}
        Date of Deliv:{date_of_delivery}

        Click the link below to reorder:
        ---------------------------
        http://127.0.0.1:8000/supplier/{St.id}
        ----------------------------
        
        


Best regards,
Skullcandy Team
'''




        send_mail_from_website(subject,message,supplier_detail.email)
        print(message)
        
    
        return HttpResponse(pop_message('/adminpage','Requested for product'))  # Replace with your success URL

    suplier=Supplier.objects.all()
    context={
        'suppliers':suplier
    }
    
    return render(request,'send_suopplier_request.html',context)

def supplier_replay(request,id):
    print(id)
    order_detail=Supplier_order.objects.get(id=id)
    print(order_detail.supplier_id.name)
    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        date_of_delivery = request.POST.get('date_of_delivery')
        status = request.POST.get('status')
        
        if quantity:
            order_detail.quantity = quantity
        if date_of_delivery:
            order_detail.date_of_delivery = date_of_delivery
        if status:
            order_detail.status = status
        order_detail.save()
        context={
        'order_detail':order_detail

        }
        
        return render(request,'supplier_success.html',context)
        

    context={        

        'order_detail':order_detail

    }
    return render(request,'supplier.html',context)


# views.py
from django.shortcuts import render
from .models import Supplier_order

def supplier_replies(request):
    orders = Supplier_order.objects.all()
    context = {
        'orders': orders
    }
    return render(request, 'supplier_replies.html', context)

def supplier_replay(request, id):
    order_detail = Supplier_order.objects.get(id=id)
    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        date_of_delivery = request.POST.get('date_of_delivery')
        status = request.POST.get('status')
        
        if quantity:
            order_detail.quantity = quantity
        if date_of_delivery:
            order_detail.date_of_delivery = date_of_delivery
        if status:
            order_detail.status = status
        order_detail.save()
        
        context = {'order_detail': order_detail}
        return render(request, 'supplier_success.html', context)

    context = {'order_detail': order_detail}
    return render(request, 'supplier.html', context)


def welcome(request):
    return render(request, 'welcome.html')



import google.generativeai as genai
from django.shortcuts import render, redirect
from django.urls import reverse

# Configure Gemini API key
genai.configure(api_key="AIzaSyDchGl9bAAz2y3uXkTQ8znlo-SEgUYUGWc")

# Create the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

from django.shortcuts import render, redirect
from django.urls import reverse
import google.generativeai as genai

# Configure Google Gemini API
api_key = os.getenv("AIzaSyDchGl9bAAz2y3uXkTQ8znlo-SEgUYUGWc", "AIzaSyCEaj-xKRhX36YEFDMyMLr4elcrYuir9I0")
genai.configure(api_key=api_key)

# Configure the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)
@login_required(login_url=user_login)
def medical_advisor_view(request):
    if request.method == 'POST':
        condition = request.POST.get('condition')
        symptoms = request.POST.get('symptoms')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        medicine_suggestion = request.POST.get('medicine_suggestion') == 'yes'
        
        # Prepare the message with input values for the chatbot prompt
        chat_history = [
            {
                "role": "user",
                "parts": [
                    f"Act as a medical adviser. The user can input the Condition, Symptoms, Age, and Gender. Based on that, suggest the treatment and any relevant medicine (if requested) with clear instructions.\n\n"
                    f"Condition: {condition}\n"
                    f"Symptoms: {symptoms}\n"
                    f"Age: {age}\n"
                    f"Gender: {gender}\n"
                ]
            },
            {
                "role": "model",
                "parts": [
                    "I will act as a medical advisor and provide suggestions based on the provided information. Please note this is not a substitute for real medical advice. Now processing the request...\n"
                ]
            }
        ]
        
        # Send the message depending on whether the user asked for medicine suggestion or not
        if medicine_suggestion:
            prompt = (
                f"Condition: {condition}\n"
                f"Symptoms: {symptoms}\n"
                f"Age: {age}\n"
                f"Gender: {gender}\n"
                "Please suggest the appropriate medicine, dosage, and method. Also specify if the medicine is suitable for certain age groups."
            )
        else:
            prompt = (
                f"Condition: {condition}\n"
                f"Symptoms: {symptoms}\n"
                f"Age: {age}\n"
                f"Gender: {gender}\n"
                "Please provide a method of treatment without medicine suggestions."
            )

        # Start a chat session with the model
        chat_session = model.start_chat(history=chat_history)
        response = chat_session.send_message(prompt)

        # Format the response to be more readable (line by line)
        result = response.text.strip().replace(". ", ".\n")  # Adding line breaks after sentences
        
        # You can further improve the formatting based on specific patterns in the response
        result_lines = result.split("\n")
        formatted_result = "\n".join([f"- {line.strip()}" for line in result_lines if line.strip()])

        return redirect(f"{reverse('advice_results')}?advice={formatted_result}")

    return render(request, 'medical_advisor.html')


def advice_results_view(request):
    advice = request.GET.get('advice', '')
    return render(request, 'advice_results.html', {'result': advice})

# views.py

from django.shortcuts import render, get_object_or_404, redirect
from .models import Doctor, DoctorAvailability, Appointment
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import now
from django.core.mail import send_mail  # For sending email notifications
from .models import Doctor, DoctorAvailability, Appointment

@login_required(login_url=user_login)
def doctor_list(request):
    doctors = Doctor.objects.all()
    return render(request, 'doctor_list.html', {'doctors': doctors})

@login_required
def doctor_availability(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    availability = DoctorAvailability.objects.filter(doctor=doctor, date__gte=now().date())
    return render(request, 'doctor_availability.html', {'doctor': doctor, 'availability': availability})

@login_required
def book_appointment(request, availability_id):
    availability = get_object_or_404(DoctorAvailability, id=availability_id)
    if request.method == 'POST':
        # Book the appointment
        appointment = Appointment.objects.create(
            user=request.user,
            doctor=availability.doctor,
            availability=availability,
            appointment_time=availability.date
        )
        # Send a confirmation email
        send_mail(
            'Appointment Confirmation',
            f'Your appointment with Dr. {availability.doctor.name} on {availability.date} is confirmed.',
            'admin@consultation.com',
            [request.user.email],
            fail_silently=False,
        )
        return redirect('appointment_success')

    return render(request, 'book_appointment.html', {'availability': availability})

@login_required
def appointment_success(request):
    # Get the latest appointment for success confirmation
    latest_appointment = Appointment.objects.filter(user=request.user).latest('appointment_time')
    return render(request, 'appointment_success.html', {'appointment': latest_appointment})

@login_required
def cancel_appointments(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    if request.method == 'POST':
        appointment.status = 'Cancelled'
        appointment.save()
        # Notify the user via email
        send_mail(
            'Appointment Cancelled',
            f'Your appointment with Dr. {appointment.doctor.name} on {appointment.appointment_time} has been cancelled.',
            'admin@consultation.com',
            [request.user.email],
            fail_silently=False,
        )
        return redirect('profile')

    return render(request, 'cancel_appointment.html', {'appointment': appointment})

@login_required
def reschedule_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    if request.method == 'POST':
        new_date = request.POST.get('new_date')
        appointment.appointment_time = new_date
        appointment.save()
        # Send reschedule notification
        send_mail(
            'Appointment Rescheduled',
            f'Your appointment with Dr. {appointment.doctor.name} has been rescheduled to {new_date}.',
            'admin@consultation.com',
            [request.user.email],
            fail_silently=False,
        )
        return redirect('profile')

    return render(request, 'reschedule_appointment.html', {'appointment': appointment})

@login_required
def medical_advisor_result_view(request):
    result = request.session.get('result', None)
    error = None
    if not result:
        error = "No result found. Please try again."
    
    return render(request, 'myapp/medical_advisor_result.html', {'result': result, 'error': error})


#visuals
# views.py
from django.shortcuts import render
import matplotlib.pyplot as plt
import io
import base64

def create_scatter_plot():
    fig, ax = plt.subplots()
    ax.scatter([1, 2, 3, 4], [10, 20, 25, 30])
    ax.set_title('Sample Scatter Plot')
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()
    return image_base64

def create_bar_chart():
    fig, ax = plt.subplots()
    categories = ['A', 'B', 'C', 'D']
    values = [5, 15, 25, 10]
    ax.bar(categories, values, color='skyblue')
    ax.set_title('Sample Bar Chart')
    ax.set_xlabel('Categories')
    ax.set_ylabel('Values')
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()
    return image_base64

def create_pie_chart():
    fig, ax = plt.subplots()
    labels = ['A', 'B', 'C', 'D']
    sizes = [20, 30, 25, 25]
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    ax.set_title('Sample Pie Chart')
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()
    return image_base64

def visuals(request):
    scatter_plot = create_scatter_plot()
    bar_chart = create_bar_chart()
    pie_chart = create_pie_chart()
    
    context = {
        'scatter_plot': scatter_plot,
        'bar_chart': bar_chart,
        'pie_chart': pie_chart,
    }
    
    return render(request, 'visuals.html', context)


#admin aprove appointments
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.core.mail import send_mail
from django.conf import settings
from .models import Appointment

@staff_member_required
def admin_appointment_list(request):
    appointments = Appointment.objects.all().order_by('-appointment_time')
    context = {
        'appointments': appointments
    }
    return render(request, 'admin_appointment_list.html', context)

@staff_member_required
def approve_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    if request.method == 'POST':
        # Update the appointment status
        appointment.status = 'Approved'
        appointment.save()

        # Send email notification
        subject = 'Appointment Approved'
        message = f'Your appointment with Dr. {appointment.doctor.name} has been approved! ' \
                  f'Details: {appointment.appointment_time}. ' \
                  f'Join the video call using this link: [INSERT_VIDEO_CALL_LINK]'
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [appointment.user.email],
            fail_silently=False,
        )

        return redirect('admin_appointment_list')  # Redirect to the appointment list

    context = {
        'appointment': appointment
    }
    return render(request, 'approve_appointment.html', context)


#visualisation

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import PatientData
from .forms import PatientDataForm
import json
import csv
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
from django.contrib.auth.decorators import login_required

# Health status levels for sugar, pressure, and cholesterol
SUGAR_LEVELS = {
    'normal': (70, 130),
    'high': (131, 200),
    'low': (0, 69)
}

PRESSURE_LEVELS = {
    'normal': (90, 120),
    'high': (121, 140),
    'low': (0, 89)
}

CHOLESTEROL_LEVELS = {
    'normal': (125, 200),
    'high': (201, 240),
    'low': (0, 124)
}

# Function to get health status based on predefined levels
def get_health_status(value, levels):
    if levels['normal'][0] <= value <= levels['normal'][1]:
        return 'Normal'
    elif levels['high'][0] <= value <= levels['high'][1]:
        return 'High'
    else:
        return 'Low'

# View to handle the patient data form submission
@login_required
def patient_form(request):
    if request.method == 'POST':
        form = PatientDataForm(request.POST)
        if form.is_valid():
            patient_data = form.save(commit=False)
            patient_data.user = request.user  # Associate the patient data with the logged-in user
            patient_data.save()  # Save the instance
            return redirect('patient_data')
    else:
        form = PatientDataForm()
    return render(request, 'patient_form.html', {'form': form})

# View to display the patient data for the logged-in user
@login_required
def patient_data(request):
    data = PatientData.objects.filter(user=request.user).order_by('-date')

    data_list = []
    for item in data:
        sugar_status = get_health_status(item.sugar_rate, SUGAR_LEVELS)
        pressure_status = get_health_status(item.pressure, PRESSURE_LEVELS)
        cholesterol_status = get_health_status(item.cholesterol_level, CHOLESTEROL_LEVELS)  # New status

        data_list.append({
            'name': item.name,
            'age': item.age,
            'gender': item.gender,
            'date': item.date.strftime('%Y-%m-%d'),
            'sugar_rate': item.sugar_rate,
            'pressure': item.pressure,
            'disease_affected': item.disease_affected,
            'cholesterol_level': item.cholesterol_level,  # Updated field
            'sugar_status': sugar_status,
            'pressure_status': pressure_status,
            'cholesterol_status': cholesterol_status  # Updated status
        })

    json_data = json.dumps(data_list)

    context = {
        'data': data,
        'json_data': json_data,
        'data_list': data_list
    }
    return render(request, 'patient_data.html', context)

# CSV Download
@login_required
def download_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="patient_data.csv"'

    writer = csv.writer(response)
    writer.writerow(['Name', 'Age', 'Gender', 'Date of Record', 'Sugar Rate', 'Pressure', 'Disease Affected', 'Cholesterol Level'])

    patients = PatientData.objects.filter(user=request.user).order_by('-date')
    for patient in patients:
        writer.writerow([
            patient.name,
            patient.age,
            patient.gender,
            patient.date.strftime('%Y-%m-%d'),
            patient.sugar_rate,
            patient.pressure,
            patient.disease_affected,
            patient.cholesterol_level  # Added cholesterol level
        ])

    return response

# PDF Download
@login_required
def download_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="patient_data.pdf"'
    
    p = canvas.Canvas(response, pagesize=letter)
    p.drawString(100, 750, "Patient Data Report")
    p.drawString(100, 730, "Name       Age       Gender       Date       Sugar Rate       Pressure       Disease Affected       Cholesterol Level")

    patients = PatientData.objects.filter(user=request.user).order_by('-date')
    y = 710
    for patient in patients:
        p.drawString(100, y, f"{patient.name}       {patient.age}       {patient.gender}       {patient.date.strftime('%Y-%m-%d')}       {patient.sugar_rate}       {patient.pressure}       {patient.disease_affected}       {patient.cholesterol_level}")
        y -= 20

    p.showPage()
    p.save()
    return response



#v1
import plotly.graph_objs as go
from django.shortcuts import render
from .forms import TimelineForm
import datetime

def create_timeline(symptom_date, diagnosis_date, treatment_date, disease_name):
    events = ['Symptom Onset', 'Diagnosis', 'Treatment Start']
    dates = [symptom_date, diagnosis_date, treatment_date]
    
    fig = go.Figure()

    # Create timeline events as markers
    fig.add_trace(go.Scatter(
        x=dates,
        y=[1, 2, 3],  # Y-values just for spacing on the chart
        mode='markers+lines',
        marker=dict(color='green', size=10),
        text=events
    ))

    fig.update_layout(
        title=f"Timeline for {disease_name}",
        xaxis_title="Date",
        yaxis_title="Events",
        yaxis=dict(tickvals=[1, 2, 3], ticktext=events),
        xaxis=dict(type='date')
    )
    
    # Return the Plotly HTML
    return fig.to_html(full_html=False)

def timeline_view(request):
    if request.method == 'POST':
        form = TimelineForm(request.POST)
        if form.is_valid():
            disease_name = form.cleaned_data['disease_name']
            symptom_date = form.cleaned_data['symptom_start_date']
            diagnosis_date = form.cleaned_data['diagnosis_date']
            treatment_date = form.cleaned_data['treatment_start_date']

            timeline_plot = create_timeline(symptom_date, diagnosis_date, treatment_date, disease_name)

            return render(request, 'timeline.html', {
                'form': form,
                'timeline_plot': timeline_plot
            })
    else:
        form = TimelineForm()

    return render(request, 'timeline.html', {'form': form})

#v2
from django.shortcuts import render
from .forms import OutcomeForm
import plotly.graph_objs as go
import plotly.io as pio
import random

def generate_comparison_chart(age, gender, severity):
    # For demonstration purposes, generating dummy data
    # Replace this with actual data from your prediction model
    
    age_groups = ['<20', '20-40', '40-60', '>60']
    recovery_times = [random.randint(5, 15), random.randint(6, 12), random.randint(10, 20), random.randint(12, 25)]
    gender_groups = ['Male', 'Female']
    
    # Create the bar chart
    fig = go.Figure()

    # Age Group Data
    fig.add_trace(go.Bar(
        x=age_groups,
        y=recovery_times,
        name='Recovery Time by Age Group',
        marker_color='lightsalmon'
    ))

    # Gender Group Data (dummy values for now)
    gender_recovery = [random.randint(5, 15), random.randint(6, 12)]
    fig.add_trace(go.Bar(
        x=gender_groups,
        y=gender_recovery,
        name='Recovery Time by Gender',
        marker_color='lightblue'
    ))

    # Add layout
    fig.update_layout(
        title=f"Outcome Comparison for {age}-year-old {gender}",
        xaxis_title="Demographics",
        yaxis_title="Recovery Time (days)",
        barmode='group'
    )

    # Return the Plotly figure as HTML
    return pio.to_html(fig, full_html=False)

def outcome_view(request):
    if request.method == 'POST':
        form = OutcomeForm(request.POST)
        if form.is_valid():
            age = form.cleaned_data['age']
            gender = form.cleaned_data['gender']
            severity = form.cleaned_data['symptom_severity']

            # Generate the comparison chart based on user input
            comparison_chart = generate_comparison_chart(age, gender, severity)

            return render(request, 'outcome_comparison.html', {
                'form': form,
                'comparison_chart': comparison_chart
            })
    else:
        form = OutcomeForm()

    return render(request, 'outcome_comparison.html', {'form': form})
    

import google.generativeai as genai

# Configure your Google API key
GOOGLE_API_KEY = 'AIzaSyAnOvp3Yj0GVKeZAuXMDC2v9l7OtiQ3g9U'
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize the Generative Model
model = genai.GenerativeModel('gemini-pro')



@login_required(login_url=user_login)
def chat_home(request):
    # Fetch chat history for the logged-in user
    chat_history = ChatHistory.objects.filter(user=request.user).order_by('created_at')

    if request.method == 'POST':
        user_input = request.POST.get('userInput').strip()

        if user_input:
            try:
                # Generate response using Google Generative AI
                response = model.generate_content(user_input)
                bot_response = response.text

                # Save user input and bot response to the database
                ChatHistory.objects.create(
                    user=request.user,
                    message_input=user_input,
                    bot_response=bot_response
                )

            except Exception as e:
                messages.warning(request, f"An error occurred: {str(e)}")
        
        return redirect('chat_home')

    context = {
        'get_history': chat_history,
        'messages': messages.get_messages(request)
    }

    return render(request, 'chat.html', context)


def patient_data_visualization(request):
    # Get the current logged-in user
    current_user = request.user
    
    # Retrieve patient data for the logged-in user
    data_list = PatientData.objects.filter(user=current_user)
    
    # Prepare JSON data for Chart.js
    json_data = [
        {
            'name': patient.name,
            'date': patient.date,
            'sugar_rate': patient.sugar_rate,
            'pressure': patient.pressure,
            'curability_level': patient.curability_level
        } 
        for patient in data_list
    ]
    
    return render(request, 'patient_data.html', {
        'data_list': data_list,
        'json_data': json_data
    })



    #doctor
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.utils.timezone import now
from .models import Appointment, DoctorAvailability

@login_required
def user_appointment_list(request):
    # Get all appointments for the logged-in user
    appointments = Appointment.objects.filter(user=request.user).order_by('-appointment_time')
    return render(request, 'user_appointment_list.html', {'appointments': appointments})

@login_required
def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, user=request.user)
    if request.method == 'POST':
        # Cancel the appointment by updating the status
        appointment.status = 'Cancelled'
        appointment.save()

        # Send an email notification for cancellation
        send_mail(
            'Appointment Cancelled',
            f'Your appointment with Dr. {appointment.doctor.name} on {appointment.appointment_time} has been cancelled.',
            'admin@consultation.com',
            [request.user.email],
            fail_silently=False,
        )
        return redirect('user_appointment_list')

    return render(request, 'cancel_appointment.html', {'appointment': appointment})

# views.py
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from django.shortcuts import render
from io import BytesIO
import base64
from .models import Doctor, DoctorAvailability, PatientData, Product

def visualizations(request):
    # Get data for doctors
    doctors = Doctor.objects.all()
    doctor_names = [doctor.name for doctor in doctors]
    specializations = [doctor.specialization for doctor in doctors]

    # Count of doctors by specialization
    specialization_counts = pd.Series(specializations).value_counts()

    # Create a bar chart for doctor specializations
    plt.figure(figsize=(10, 6))
    sns.barplot(x=specialization_counts.index, y=specialization_counts.values, palette='viridis')
    plt.title('Number of Doctors by Specialization')
    plt.xlabel('Specialization')
    plt.ylabel('Number of Doctors')
    plt.xticks(rotation=45)
    # Save plot to a BytesIO object
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_png = buf.getvalue()
    buf.close()
    chart1 = base64.b64encode(image_png).decode('utf-8')

    # Get patient data
    patients = PatientData.objects.all()
    patient_data = {
        "sugar_rate": [patient.sugar_rate for patient in patients],
        "pressure": [patient.pressure for patient in patients],
        "cholesterol_level": [patient.cholesterol_level for patient in patients],
    }
    patient_df = pd.DataFrame(patient_data)

    # Boxplot for patient health metrics
    melted_patient_data = patient_df.melt(value_vars=['sugar_rate', 'pressure', 'cholesterol_level'], 
                                           var_name='Metric', value_name='Value')
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=melted_patient_data, x='Metric', y='Value', palette='pastel')
    plt.title('Distribution of Patient Health Metrics')
    plt.xlabel('Health Metric')
    plt.ylabel('Value')
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_png = buf.getvalue()
    buf.close()
    chart2 = base64.b64encode(image_png).decode('utf-8')

    # Get data for products
    products = Product.objects.all()
    product_names = [product.name for product in products]
    product_prices = [product.price for product in products]
    product_quantities = [product.quantity for product in products]

    # Create a bar chart for product prices
    plt.figure(figsize=(10, 6))
    sns.barplot(x=product_names, y=product_prices, palette='magma')
    plt.title('Product Prices')
    plt.xlabel('Product Name')
    plt.ylabel('Price')
    plt.xticks(rotation=45)
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_png = buf.getvalue()
    buf.close()
    chart3 = base64.b64encode(image_png).decode('utf-8')

    # Prepare context for the template
    context = {
        'chart1': chart1,
        'chart2': chart2,
        'chart3': chart3,
    }
    return render(request, 'visualizations1.html', context)
