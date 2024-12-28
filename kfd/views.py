from itertools import product
from django.shortcuts import render, redirect , get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from . models import *
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User,auth
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime
from django.db.models import Q
from geopy.exc import GeocoderTimedOut
from geopy.distance import geodesic
from geopy.exc import GeocoderServiceError

from geopy.geocoders import Nominatim
from django.contrib import messages
from .models import Address, Cart, Checkout, Registration
import requests
import math
from django.utils.safestring import mark_safe


def home(request):
    products = Product.objects.all()
    return render(request, 'tem/index.html', {'fgt': products})


def register_admin(request):
    if request.method == 'POST':
        # Get form data
        email = request.POST.get('email')
        psw = request.POST.get('password')
        user_name = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        # Check if the user role is 'admin'
        if Registration.objects.filter(User_role='admin').exists():
            messages.error(request, 'You are not allowed to register as admin')
            return redirect('index')

        # Check if the email already exists
        if Registration.objects.filter(user__email=email).exists():
            messages.error(request, 'User already exists with this email')
            return redirect('admin')

        # Check if the username already exists
        if User.objects.filter(username=user_name).exists():
            messages.error(request, 'Username taken. Please try another')
            return redirect('admin')

        # Create the new user
        user = User.objects.create_user(
            username = user_name,
            email = email,
            password = psw,
            first_name = first_name,
            last_name = last_name
        )

        # Create a registration entry
        registration = Registration(
            user=user,
            Password=psw,  # Consider hashing passwords instead
            User_role='admin'
        )
        registration.save()

        messages.success(request, 'You have successfully registered as admin')
        return redirect('index')

    else:
        return render(request, 'register_admin.html')


def login(request):
    print(request.method)
    if request.method == 'POST':
        username = request.POST.get("user_name")
        password = request.POST.get("pword")
        user = auth.authenticate(username=username, password=password)
        if user is None:
            messages.success(request, 'Invalid credentials')
            return redirect('login')
        auth.login(request, user)
        if Registration.objects.filter(user=user, Password=password).exists():
            logs = Registration.objects.filter(user=user, Password=password)
            for value in logs:
                user_id = value.id
                usertype = value.User_role
                if usertype == 'admin':
                    request.session['logg'] = user_id
                    return redirect('admin_home')
                elif usertype == 'custmer':
                    request.session['logg'] = user_id
                    return redirect('customer_home')
                elif usertype == 'supplier':
                    request.session['logg'] = user_id
                    return redirect('supplier_home')
                else:
                    messages.success(request, 'Your access to the website is blocked. Please contact admin')
                    return redirect('login')
        else:
            messages.success(request, 'Username or password entered is incorrect')
            return redirect('login')
    else:
        return render(request, 'login.html')


def register_custmer(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        psw = request.POST.get('password')
        confirm_psw = request.POST.get('confirm-password')

        # Check if the email already exists in the Registration model
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists. Please use a different email.')
            return redirect('register_custmer')

        # Check if the username is taken
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username taken. Please try another.')
            return redirect('register_custmer')

        # Check if passwords match
        if psw != confirm_psw:
            messages.error(request, 'Passwords do not match. Please try again.')
            return redirect('register_custmer')

        # Create the user
        user = User.objects.create_user(username=username, email=email, password=psw, first_name=first_name, last_name=last_name)

        # Create registration entry
        registration_entry = Registration(user=user, Password=psw, User_role='custmer')
        registration_entry.save()

        messages.success(request, 'You have successfully registered as customer.')
        return redirect('index')

    return render(request, 'register_custmer.html')


def customer_home(request):
    products = Product.objects.all()
    return render(request, 'customer_home.html', {'fgt': products})


@login_required
def admin_home(request):
    fgt = Product.objects.all()
    return render(request, 'admin_home.html', {'fgt': fgt})


def iteams(request):
    return render(request, 'iteams.html')


def edit_product_adm(request, id):
    product = get_object_or_404(Product, id=id)  # Correct: lowercase instance
    if request.method == 'POST':
        product.product_name = request.POST['product_name']  # Accessing field of instance
        product.product_price = request.POST['product_price']
        if 'photo' in request.FILES:
            product.photo = request.FILES['photo']
        product.save()
        return redirect('admin_home')
    return render(request, 'edit_product_adm.html', {'product': product})


def add_product_adm(request):
    if request.method == 'POST':
        product_name = request.POST.get("product_name")
        product_price = request.POST.get("product_price")
        photo = request.FILES["photo"]
        fs = FileSystemStorage()
        fs.save(photo.name,photo)
        if Product.objects.filter(product_name = product_name).exists():
            messages.error(request, 'Product with this name already exists.')
            return redirect('add_product_adm')

        product = Product(product_name = product_name, product_price = product_price, photo = photo)
        product.save()

        messages.success(request, 'Food added successfully')
        return redirect('admin_home')
    else:
        return render(request, 'add_product_adm.html')


@login_required
def logout(request):
    auth.logout(request)
    return redirect('index')


def delete_product_adm(request, id):
    product = get_object_or_404(Product, id=id)
    product.delete()
    return redirect('admin_home')


def index(request):
    # Retrieve all products from the database
    products = Product.objects.all()
    return render(request, 'index.html', {'fgt': products})


@login_required
def custmer_cart(request, product_id=None):
    if product_id:
        product = Product.objects.get(id = product_id)
        Cart.objects.get_or_create(
            product = product,
            user = request.user,
            defaults = {'product_name': product.product_name}
        )

    cart_items = Cart.objects.filter(user = request.user)
    total_price = sum(item.total_price for item in cart_items)

    saved_addresses = Address.objects.filter(user=request.user)

    return render(request, 'custmer_cart.html', {
        'cart_items': cart_items,
        'tot_price': total_price,
         'saved_addresses': saved_addresses
    })


def edit_addr_cust(request, id):
    cvc = Address.objects.get(id = id)
    if request.method == 'POST':
        house_number = request.POST.get('house_number')
        apartment = request.POST.get('apartment')
        city = request.POST.get('city')
        postal_code = request.POST.get('postal_code')
        state = request.POST.get('state')
        latitude1 = request.POST.get('latitude1')
        longitude1 = request.POST.get('longitude1')
        cvc.house_number = house_number
        cvc.apartment = apartment
        cvc.city = city
        cvc.postal_code = postal_code
        cvc.state = state
        cvc.longitude = longitude1
        cvc.latitude = latitude1
        cvc.save()
        messages.success(request,'Address edited successfully')
        return redirect('custmer_cart')
    return render(request,'edit_addr_cust.html',{'cvc':cvc})

@login_required
def del_addr_cust(request, id):
    Address.objects.get(id = id).delete()
    return redirect('custmer_cart')


def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    if request.user.is_authenticated:
        cart_item, created = Cart.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={'quantity': 1, 'product_name': product.product_name}
        )
        if not created:
            cart_item.quantity += 1
            cart_item.save()
    return redirect('custmer_cart')


def update_cart_decr_ajax(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        cart_item = get_object_or_404(Cart, id=item_id, user=request.user)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()

        cart_items = Cart.objects.filter(user=request.user)
        tot_price = sum(item.total_price for item in cart_items)

        return JsonResponse({
            'new_quantity': cart_item.quantity,
            'tot_price': tot_price,
            'cart_items': [
                {
                    'id': item.id,
                    'quantity': item.quantity,
                    'total_price': item.total_price,
                    'product_price': item.product.product_price,
                } for item in cart_items
            ],
        })


def update_cart_incr_ajax(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        cart_item = get_object_or_404(Cart, id=item_id, user=request.user)
        cart_item.quantity += 1
        cart_item.save()

        cart_items = Cart.objects.filter(user=request.user)
        tot_price = sum(item.product.product_price * item.quantity for item in cart_items)

        return JsonResponse({
            'new_quantity': cart_item.quantity,
            'tot_price': tot_price,
            'cart_items': [
                {
                    'id': item.id,
                    'quantity': item.quantity,
                    'total_price': item.total_price,
                    'product_price': item.product.product_price,
                } for item in cart_items
            ],
        })


def remove_from_cart(request, item_id):
    # Fetch the cart item by ID and delete it
    cart_item = Cart.objects.get(id=item_id)
    cart_item.delete()
    return redirect('custmer_cart')


def contact_mail(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    message = request.POST.get('message')
    subject = f"New message from {name}"
    body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
    subject_to_cstmr = 'Thank You for Reaching Out to Tasty Roots'
    bdy_to_cstmr = (
     '''
     Dear '''+name+''',
     Thank you for contacting us at Tasty Roots! We have received your message and will get back
     to you as soon as possible.
     Whether you have a question about our menu, reservations, or special events, we’re here to help
     make your experience with us exceptional.
     In the meantime, feel free to explore our website for more details or follow us on social media for
     the latest updates and promotions.
     We look forward to serving you soon!
     Warm regards,
     Front desk
     Personal relations officer
     Tasty Roots
     7034456721
     tastyroots@gmail.com'''
    )

    from_email = settings.EMAIL_HOST_USER
    to_email = [from_email]

    from_email1 = settings.EMAIL_HOST_USER
    to_email1 =[email]

    try:
        send_mail(subject, body, from_email, to_email, fail_silently=False)
        send_mail(subject_to_cstmr, bdy_to_cstmr, from_email1, to_email1, fail_silently=False)
        messages.success(request,'Email sent successfully!')
        return redirect('index')
    except Exception as e:
        kjk = "An error occurred: "+ str(e)
        messages.error(request, mark_safe(kjk))
        return redirect('index')


def get_current_address(latitude, longitude):
    reverse_geocode_url = f"https://nominatim.openstreetmap.org/reverse?lat={latitude}&lon={longitude}&format=json&addressdetails=1"

    headers = {
        'User-Agent': 'kfd/mruthulammvk3@gmail.com)'  # Replace with your app name and email
    }

    try:
        response = requests.get(reverse_geocode_url, headers=headers, timeout=5)
        response.raise_for_status()  # Raise an error for bad responses

        # Print the raw response for debugging
        print(response.text)

        # Check if the response contains valid data
        if response.status_code == 200:
            data = response.json()
            if 'error' in data:
                return 'Unknown Location'
            # Make sure 'display_name' is in the response
            return data.get('display_name', 'Unknown Location')
        else:
            return 'Unknown Location'

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return 'Unknown Location'


@login_required
def checkout(request):
    if 'logg' not in request.session:
        return redirect('login')

    saved_addresses = Address.objects.filter(user = request.user)
    checkout_items = Cart.objects.filter(user = request.user)
    total_price = sum(item.product.product_price * item.quantity for item in checkout_items)

    if request.method == 'POST':
        location_type = request.POST.get('location_type')
        entered_price = request.POST.get('tot_amt1')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        if (not entered_price) or (not entered_price.isdigit()) or (float(entered_price) != total_price):
            messages.error(request, "Entered amount does not match the total price.")
            return redirect('custmer_cart')

        if location_type != 'current_location':
            location_type = int(location_type)
            selected_address = Address.objects.get(id = location_type)
            for item in checkout_items:
                Checkout.objects.create(
                        chekout_reg = Registration.objects.get(id = request.session['logg']),
                        product = item.product,
                        quantity = item.quantity,
                        price = item.product.product_price,
                        chk_address = selected_address,
                    )

            checkout_items.delete()
            messages.success(request, "Thank you for your purchase!")
            return redirect('customer_home')

        elif location_type == 'current_location':
            if (not latitude) or (not longitude):
                messages.error(request, "Unable to fetch current location. Please try again.")
                return redirect('custmer_cart')

            current_address = get_current_address(latitude, longitude)

            for item in checkout_items:
                Checkout.objects.create(
                    chekout_reg = Registration.objects.get(id=request.session['logg']),
                    product = item.product,
                    quantity = item.quantity,
                    price = item.product.product_price,
                    current_address = current_address,
                    latitude = latitude,
                    longitude = longitude,
                )
            checkout_items.delete()
            messages.success(request, "Thank you for your purchase!")
            return redirect('customer_home')

        else:
            messages.error(request, "Please select a valid address option.")
            return redirect('custmer_cart')

    return render(request, 'custmer_cart.html', {'saved_addresses': saved_addresses,'checkout_items': checkout_items,'total_price': total_price,})


def checkout_new_adr(request):
    tot_amt = request.POST.get('tot_amt')
    latitude = request.POST.get('latitude1')
    longitude = request.POST.get('longitude1')
    house_number = request.POST.get('house_number')
    apartment = request.POST.get('apartment')
    city = request.POST.get('city')
    state = request.POST.get('state')
    postal_code = request.POST.get('postal_code')

    if latitude and longitude:
        new_address = Address.objects.create(
            user = request.user,
            house_number = house_number,
            apartment = apartment,
            city = city,
            state = state,
            postal_code = postal_code,
            latitude = latitude,
            longitude = longitude
        )

        checkout_items = Cart.objects.filter(user = request.user)
        total_price = sum(item.product.product_price * item.quantity for item in checkout_items)

        if float(total_price) != float(tot_amt):
            messages.success(request,'Entered amount is incorrect')
            return redirect('custmer_cart')

        for item in checkout_items:
            Checkout.objects.create(
                chekout_reg = Registration.objects.get(id=request.session['logg']),
                product = item.product,
                quantity = item.quantity,
                price = item.product.product_price,
                chk_address = new_address
            )

        checkout_items.delete()
        messages.success(request, "Thank you for your purchase!")
        return redirect('customer_home')
    else:
        messages.success(request, 'Latitude and longitude cannot be fetched. Please try again.')
        return redirect('custmer_cart')


@csrf_exempt
def check_total_amount(request):
    if request.method == "POST":
        data = json.loads(request.body)
        entered_amount = float(data['entered_amount'])
        total_price = float(data['total_price'])
        # Compare entered amount with total price
        is_correct = entered_amount == total_price
        return JsonResponse({'is_correct': is_correct})


@login_required
def orders_customer(request):
    checkouts = Checkout.objects.filter(chekout_reg = request.session['logg'])
    non_delivered_orders = checkouts.filter(is_delivered_status = False)
    return render(request, 'orders_customer.html', {'checkouts': non_delivered_orders})


def custmer_order_adm(request):
    orders = Checkout.objects.all()
    return render(request, 'custmer_order_adm.html', {'orders': orders})


def approve_order(request, order_id):
    order = Checkout.objects.get(id=order_id)
    order.is_approved = True
    order.save()
    return redirect('custmer_order_adm')


def prepare_order(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(Checkout, id=order_id)
        order.is_preparing = True  # Set this to true if you are using this to track preparing state
        order.is_prepared = True    # Set this to true if you want to mark it as prepared immediately
        order.save()
        return redirect('custmer_order_adm')


def delivery_partner_arrived(request, order_id):
    order = get_object_or_404(Checkout, id=order_id)
    order.is_delivery_partner_arrived = True
    order.save()
    return redirect('custmer_order_adm')


def deliver_order(request, order_id):
    order = get_object_or_404(Checkout, id=order_id)
    order.is_delivered = True  # Set this flag to indicate that the order has been delivered
    order.save()
    return redirect('custmer_order_adm')  # Ensure this points to the correct URL name for your purchase history page


def approve_order(request, order_id):
    order = get_object_or_404(Checkout, id=order_id)
    order.is_approved = True
    order.save()
    return redirect('custmer_order_adm')


def supplier_home(request):
    products = Product.objects.all()
    cdc = Supplier_status.objects.last()
    return render(request, 'supplier_home.html', {'fgt': products, 'cdc':cdc})


def register_supplier(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        psw = request.POST.get('password')
        confirm_psw = request.POST.get('confirm-password')


        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists. Please use a different email.')
            return redirect('register_supplier')


        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username taken. Please try another.')
            return redirect('register_supplier')


        if psw != confirm_psw:
            messages.error(request, 'Passwords do not match. Please try again.')
            return redirect('register_supplier')


        user = User.objects.create_user(username=username, email=email, password=psw, first_name=first_name, last_name=last_name)


        registration_entry = Registration(user=user, Password=psw, User_role='supplier')
        registration_entry.save()

        messages.success(request, 'You have successfully registered as supplier.')
        return redirect('index')

    return render(request, 'register_supplier.html')


@csrf_exempt
@login_required
def update_status(request):
    # Ensure the user is logged in
    user_id = request.session.get('logg')
    if not user_id:
        return JsonResponse({'success': False, 'error': 'User not logged in'}, status=403)

    try:
        kmk = Registration.objects.get(id = user_id)
    except Registration.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Invalid user'}, status=404)

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            status = data.get('status')

            if status not in ['In', 'Out']:
                return JsonResponse({'success': False, 'error': 'Invalid status'}, status=400)

            # Create a new status
            new_status = Supplier_status.objects.create(in_out = status, supplier_reg = kmk)

            # Serialize the newly created status
            response_data = {
                'id': new_status.id,
                'status': new_status.in_out,
                'supplier_id': new_status.supplier_reg.id,
                'timestamp': new_status.date_time.strftime('%Y-%m-%d %H:%M:%S')  # Assuming `date_time` is a datetime field
            }

            return JsonResponse({'success': True, 'status_data': response_data}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)


@login_required
def supplier_details(request):
    srch = request.GET.get('srch','')
    date = request.GET.get('date', '')
    from_date = request.GET.get('from_date', '')
    to_date = request.GET.get('to_date', '')

    # Start with all orders
    orders = Supplier_status.objects.all()

    # Apply search across multiple fields
    if srch:
        orders = orders.filter(
            Q(supplier_reg__user__first_name__icontains = srch) |
            Q(supplier_reg__user__last_name__icontains = srch) |
            Q(supplier_reg__user__email__icontains = srch) |
            Q(in_out__icontains = srch)
        )

    # Exact date filter if 'date' is provided
    if date:
        try:
            date = datetime.strptime(date, '%Y-%m-%d').date()
            orders = orders.filter(date_time__date=date)
        except ValueError:
            pass  # Ignore invalid date input

    # Date range filter: only apply if both 'from_date' and 'to_date' are provided
    try:
        if from_date and to_date:
            # Parse dates in 'DD-MM-YYYY' format to 'YYYY-MM-DD'
            from_date = datetime.strptime(from_date, '%Y-%m-%d').date()
            to_date = datetime.strptime(to_date, '%Y-%m-%d').date()
            orders = orders.filter(date_time__date__range=(from_date, to_date))
    except ValueError:
        pass  # Ignore invalid date input

    context = {
        'supplier_statuses': orders
    }
    return render(request, 'supplier_details.html', context)


@login_required
def delete_suppl_stats_adm(request, id):
    Supplier_status.objects.get(id = id).delete()
    return redirect('supplier_detail')


def save_location(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            address = data.get('address')

            # Create a new address record with the full address
            address_record = Address.objects.create(
                user=request.user,
                address=address,  # Save the human-readable address
            )
            return JsonResponse({"success": True, "message": "Location saved successfully!"})
        except Exception as e:
            return JsonResponse({"success": False, "message": f"Error: {str(e)}"})
    return JsonResponse({"success": False, "message": "Invalid request method."})


def assign_delivary_boy(request, order_id):
    # Retrieve the order object, if not found it will raise a 404 error
    order = get_object_or_404(Checkout, id=order_id)

    # Fetch all suppliers (we will later filter them based on the most recent status)
    suppliers = Supplier_status.objects.select_related('supplier_reg')

    # Log the suppliers for debugging
    print("Filtered Suppliers (in_out='In'):")
    for supplier in suppliers:
        print(f"Supplier ID: {supplier.supplier_reg.id}, Name: {supplier.supplier_reg.user.first_name}, Status: {supplier.in_out}")

    # Filter suppliers: Only include those who have a recent 'In' status and do not have a recent 'Out' status
    valid_suppliers = []
    seen_supplier_ids = set()

    for supplier in suppliers:
        # Ensure each supplier appears only once based on their registration ID
        if supplier.supplier_reg.id not in seen_supplier_ids:
            # Fetch the supplier's latest status (most recent)
            latest_status = Supplier_status.objects.filter(
                supplier_reg=supplier.supplier_reg
            ).order_by('-date_time').first()

            # Log the latest status for debugging
            print(f"Latest Status for Supplier ID {supplier.supplier_reg.id}: {latest_status.in_out} at {latest_status.date_time}")

            # Only include suppliers whose most recent status is 'In'
            if latest_status and latest_status.in_out == "In":
                # Check if there's any 'Out' status for this supplier
                has_out_status = Supplier_status.objects.filter(
                    supplier_reg=supplier.supplier_reg,
                    in_out="Out"
                ).exists()

                # Exclude suppliers who have a recent 'Out' status but include them if their latest status is 'In'
                if not has_out_status or latest_status.in_out == "In":
                    valid_suppliers.append(supplier)
                    seen_supplier_ids.add(supplier.supplier_reg.id)

    # Log valid suppliers passed to the template for debugging
    print("Valid Suppliers Passed to Template:")
    for supplier in valid_suppliers:
        print(f"Supplier ID: {supplier.supplier_reg.id}, Name: {supplier.supplier_reg.user.first_name}")

    if request.method == 'POST':
        # Handle form submission to assign a delivery boy
        delivery_boy_id = request.POST.get('delivery_boy')

        try:
            # Get the delivery boy registration based on the ID
            delivery_boy = Registration.objects.get(id=delivery_boy_id)

            # Assign the delivery boy to the order
            order.delivery_boy = delivery_boy
            order.save()

            # Redirect to the orders page after saving
            return redirect('custmer_order_adm')  # Redirect to the orders page

        except Registration.DoesNotExist:
            # Handle case where the delivery boy does not exist
            print(f"Delivery boy with ID {delivery_boy_id} not found.")
            return redirect('supplier_home')  # Redirect to an error page or show a message to the user

    # Pass valid suppliers to the template for rendering
    return render(request, 'assign_delivary_boy.html', {
        'order': order,
        'suppliers': valid_suppliers,
    })


def supplier_assigned_orders(request):
    if not request.user.is_authenticated:
        return redirect('login')

    # Get the Registration instance for the logged-in user (the delivery boy)
    registration = Registration.objects.get(user=request.user)

    # Check the most recent Supplier_status entry for this supplier
    supplier_status = Supplier_status.objects.filter(supplier_reg=registration).last()

    # If the supplier's status is 'In', proceed to fetch assigned orders
    if supplier_status and supplier_status.in_out == 'In':
        # Get all assigned orders where delivery_boy matches the current supplier's registration
        assigned_orders = Checkout.objects.filter(delivery_boy=registration)

        return render(request, 'supplier_assigned_orders.html', {
            'assigned_orders': assigned_orders,
        })
    else:
        # If the supplier is 'Out', show a message
        return render(request, 'supplier_assigned_orders.html', {
            'assigned_orders': [],
            'message': "You are currently marked as 'Out' and have no assigned orders.",
        })


def update_order_status(request):
    if request.method == "POST":
        order_id = request.POST.get('order_id')
        status = request.POST.get('status')

        try:
            order = Checkout.objects.get(id=order_id)
        except Checkout.DoesNotExist:
            messages.error(request, "Order not found.")
            return redirect('supplier_assigned_orders')

        # Update order status based on the value
        if status == 'Out of Delivery':
            order.is_out_of_delivery = True
            order.is_delivered_status = False  # Order is not delivered yet
            order.save()

        elif status == 'Delivered':
            order.is_out_of_delivery = True  # Keep the 'out of delivery' status as True
            order.is_delivered_status = True  # Mark the order as delivered
            order.save()


        return redirect('supplier_assigned_orders')  # Redirect back to the orders page


def track_order_adm(request, order_id):
    order = get_object_or_404(Checkout, id = order_id)
    return render(request, 'track_order_adm.html', {'order': order})


def purchase_history_customer(request):
    all_orders = Checkout.objects.filter(chekout_reg__user = request.user)
    delivered_orders = all_orders.filter(is_delivered_status = True)
    non_delivered_orders = all_orders.filter(is_delivered_status = False)

    context = {
        'delivered_orders': delivered_orders,
        'non_delivered_orders': non_delivered_orders,
    }

    return render(request, 'purchase_history_customer.html', context)


@csrf_exempt
@login_required
def update_supplier_location(request):
    print('hello')  # Debug

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print('mruthula')  # Debug

            latitude = data.get('latitude')
            longitude = data.get('longitude')
            status = data.get('status')

            # Validate data
            if not all([latitude, longitude, status]):
                return JsonResponse({'error': 'Latitude, longitude, and status are required.'}, status=400)

            try:
                latitude = float(latitude)
                longitude = float(longitude)
            except ValueError:
                return JsonResponse({'error': 'Invalid latitude or longitude values.'}, status=400)

            if status != 'In':
                return JsonResponse({'error': 'Supplier must be "In" to update location.'}, status=400)

            # Ensure user has a related registration object
            registration = getattr(request.user, 'registration', None)
            if not registration:
                return JsonResponse({'error': 'No registration found for the user.'}, status=400)

            # Find the latest supplier status or create a new one
            supplier_status = Supplier_status.objects.filter(supplier_reg=registration).order_by('-date_time').first()
            if not supplier_status:
                supplier_status = Supplier_status.objects.create(
                    supplier_reg=registration,
                    in_out='Out'  # Default value
                )

            # Reverse geocode address
            geolocator = Nominatim(user_agent="kfcc_supplier_app")
            try:
                location = geolocator.reverse((latitude, longitude), language='en')
                address = location.address if location else "No address found"
            except Exception as e:
                print("Geocoding error:", e)
                address = f"Geolocation lookup failed: {e}"

            # Update the status
            supplier_status.in_out = status
            supplier_status.latitude = latitude
            supplier_status.longitude = longitude
            supplier_status.address = address
            supplier_status.save()

            print('Updated Supplier Status:', supplier_status.__dict__)  # Debug

            return JsonResponse({
                'message': 'Location updated successfully.',
                'latitude': latitude,
                'longitude': longitude,
                'address': address
            }, status=200)

        except Exception as e:
            print('Unhandled exception:', e)  # Debug
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request method.'}, status=405)


def haversine(lat1, lon1, lat2, lon2):
    return geodesic((lat1, lon1), (lat2, lon2)).km


# Function to get coordinates from address
def get_coordinates(address):
    try:
        geolocator = Nominatim(user_agent="myGeocoder")
        location = geolocator.geocode(address, timeout=10)
        if location:
            return location.latitude, location.longitude
        else:
            print("Failed to geocode the address.")
            return None, None
    except GeocoderTimedOut:
        print("Geocoding timed out. Try again later.")
        return None, None
    except GeocoderServiceError as e:
        print(f"Geocoding service error: {e}")
        return None, None


def calculate_distance(lat1, lon1, lat2, lon2):
    # Radius of Earth in kilometers
    R = 6371.0

    # Convert degrees to radians
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Calculate distance
    distance = R * c
    return distance


def track_supplier(request, checkout_id):
    order = get_object_or_404(Checkout, id=checkout_id)
    print(f"Customer Coordinates: ({order.latitude}, {order.longitude})")

    if order.latitude is None and order.chk_address:
        address = order.chk_address
        if address.latitude and address.longitude:

            order.latitude = address.latitude
            order.longitude = address.longitude
            order.save()
            print(f"Customer Coordinates Updated from Address: ({order.latitude}, {order.longitude})")
        else:
            print("Warning: Customer address coordinates are missing.")


    customer_lat = order.latitude
    customer_lon = order.longitude
    print(f"Customer Location: ({customer_lat}, {customer_lon})")


    supplier_lat = supplier_lon = None
    supplier_address = None
    if order.delivery_boy:
        supplier_status = Supplier_status.objects.filter(
            supplier_reg__User_role="supplier"
        ).order_by('-date_time').first()

        if supplier_status and supplier_status.in_out == "In":
            supplier_address = supplier_status.address
            supplier_lat = supplier_status.latitude
            supplier_lon = supplier_status.longitude


    print(f"Supplier Location: ({supplier_lat}, {supplier_lon})")


    distance = None
    if customer_lat is not None and customer_lon is not None and supplier_lat is not None and supplier_lon is not None:
        distance = calculate_distance(customer_lat, customer_lon, supplier_lat, supplier_lon)
    else:
        print("Error: Missing location data. Customer or Supplier coordinates not found.")


    context = {
        'product_name': order.product.product_name,
        'quantity': order.quantity,
        'total_price': order.price * order.quantity,
        'delivery_boy': order.delivery_boy,
        'saved_address': order.chk_address,
        'current_address': order.current_address,
        'supplier_address': supplier_address,
        'order': order,
        'distance': distance,
    }

    return render(request, 'track_supplier.html', context)


def orders_view(request):
    # Get all checkouts except those with "Delivered Successfully" status
    checkouts = Checkout.objects.exclude(is_delivered_status=True)
    return render(request, 'orders.html', {'checkouts': checkouts})



