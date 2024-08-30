from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from .forms import ProductForm
from .models import Category, Product, UserProfile,Supplier,Supplier_order
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
            user = form.save()
            login(request, user)
            registration_successful = True
            return redirect('user_login')
    else:
        form = CustomUserCreationForm()

    return render(request, 'user_register.html', {'form': form, 'registration_successful': registration_successful})

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                form.add_error(None, 'Invalid username or password')
        else:
            # Clear the password field for security reasons
            form.data = form.data.copy()
            form.data['password'] = ''
    else:
        form = AuthenticationForm()
    
    return render(request, 'user_login.html', {'form': form})




def user_logout(request):
    logout(request)
    # Redirect to the index page after logout

    return redirect('index')


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
                    return redirect('index')  # Redirect regular user to index page
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

def home(request):
    categories = Category.objects.all()
    selected_category = None
    products = Product.objects.all()

    if 'category' in request.GET:
        category_id = request.GET['category']
        if category_id:
            selected_category = Category.objects.get(pk=category_id)
            products = Product.objects.filter(category=selected_category)

    context = {
        'categories': categories,
        'selected_category': selected_category,
        'products': products,
    }
    return render(request, 'home.html', context)

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
