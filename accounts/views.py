from django.shortcuts import render, get_object_or_404 , redirect
from .models import Book, Category , Review , CartItem , Order, OrderItem
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json
from django.views.decorators.http import require_GET
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate , logout
from django.contrib import messages
from bakong_khqr import KHQR
import qrcode
from io import BytesIO
import base64
import hashlib
import requests


# Create your views here.

def index(request):
    # Get the categories by name or raise a 404 error if not found
    category_comics = get_object_or_404(Category, name='Comics & Graphic Novels')
    category_manga = get_object_or_404(Category, name='Manga & Graphic Novels')
    category_horror = get_object_or_404(Category, name='Horror')
    
    # Filter books by the given categories
    books_comics = Book.objects.filter(category=category_comics)
    books_manga = Book.objects.filter(category=category_manga)
    books_horror = Book.objects.filter(category=category_horror)

    context = {
        'books_comics': books_comics,
        'books_manga': books_manga,
        'books_horror': books_horror,
    }
    
    return render(request, 'accounts/home.html', context)


def book_detail(request, slug):

    book = get_object_or_404(Book, slug=slug)
    reviews = Review.objects.filter(book=book)
    
     # Get the category by name or raise a 404 error if not found
     #To show other books at the bottom of the page
    category_name = 'Comics & Graphic Novels'
    category = get_object_or_404(Category, name=category_name)
    books = Book.objects.filter(category=category)

    context = {
        'book': book,
        'reviews': reviews,
        'books': books,
    }
    return render(request, 'accounts/show.html', context)

def show_by_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    books = Book.objects.filter(category=category)
    context = {
        'category': category,
        'books': books
    }
    return render(request, 'accounts/show_by_category.html', context)


def search(request):
    return render(request, 'accounts/search.html')  

def search_books(request):
    query = request.GET.get('q', '') #retrieves the value of the query parameter q from the URL. If the q parameter is not present in the URL, it defaults to an empty string ''.
    if query:
        books = Book.objects.filter(title__icontains=query) #perform case-insensitive search on title
        #then we got a book object
        results = []
        for book in books:
            results.append({
                'title': book.title,
                'author': book.author.name,
                'price': book.price,
                'cover_image': book.cover_image,
                'slug': book.slug,
                'id': book.id,
            })
        return JsonResponse(results, safe=False) #safe false allows the response to be a list (array) instead of a dictionary (object).
    return JsonResponse([], safe=False)

def new_books(request):
   
    books = Book.objects.all().order_by('-id')  # Order by primary key in descending order
    context = {
        'books': books
    }
    return render(request, 'accounts/show_by_category.html', context)

@require_POST
def add_to_cart(request, book_id):
    # Parse JSON data from the request body
    data = json.loads(request.body)
    quantity = data.get('quantity', 1)  # Default to 1 if quantity is not provided

    book = get_object_or_404(Book, id=book_id)
    
    # Ensure the user has a session key
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key

    if request.user.is_authenticated:
        # Associate cart item with the logged-in user
        cart_item, created = CartItem.objects.get_or_create(
            Book=book,
            user=request.user,
            defaults={'quantity': quantity}
        )
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
    else:
        # Use session_key for guest users
        cart_item, created = CartItem.objects.get_or_create(
            Book=book,
            session_key=session_key,
            defaults={'quantity': quantity}
        )
        if not created:
            cart_item.quantity += quantity
            cart_item.save()

    # Return a JSON response for AJAX
    return JsonResponse({'success': True})

@require_GET
def is_in_cart(request, book_id):
    if request.user.is_authenticated:
        # Check if the book exists in the logged-in user's cart
        in_cart = CartItem.objects.filter(user=request.user, Book_id=book_id).exists()
    else:
        # Check if the book exists in the guest user's cart (session-based)
        session_key = request.session.session_key
        if not session_key:
            return JsonResponse({'in_cart': False})

        in_cart = CartItem.objects.filter(session_key=session_key, Book_id=book_id).exists()

    return JsonResponse({'in_cart': in_cart})

@require_GET
def cart_item_count(request):
    if request.user.is_authenticated:
        # Count items linked to logged-in user
        count = CartItem.objects.filter(user=request.user).count()
    else:
        # Use session_key for guest users
        session_key = request.session.session_key
        if not session_key:
            return JsonResponse({'count': 0})

        count = CartItem.objects.filter(session_key=session_key).count()

    return JsonResponse({'count': count})


def cart_items(request):
    if request.user.is_authenticated:
        # Fetch cart items linked to the user
        cart_items = CartItem.objects.filter(user=request.user)
    else:
        # Use session_key for guest users
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key

        cart_items = CartItem.objects.filter(session_key=session_key)

    # Calculate total price
    total_price = sum(item.Book.price * item.quantity for item in cart_items)

    return render(request, 'accounts/cart_items.html', {'cart_items': cart_items, 'total_price': total_price})

@require_POST
def delete_cart_item(request, book_id):
    """
    Deletes a cart item for the logged-in user or session-based user.
    """
    if request.user.is_authenticated:
        # Delete the cart item associated with the logged-in user
        CartItem.objects.filter(user=request.user, Book_id=book_id).delete()
    else:
        # Delete the cart item associated with the session key for guest users
        session_key = request.session.session_key
        if session_key:
            CartItem.objects.filter(session_key=session_key, Book_id=book_id).delete()

    # Return a JSON response for AJAX or redirect for non-AJAX requests
    return redirect('cart_items')  # Redirect to the cart items page after deletion

@require_POST
def update_cart_item(request, book_id):
    """
    Updates the quantity of a cart item for the logged-in user or session-based user.
    """
    new_quantity = int(request.POST.get('quantity', 1))  # Get the new quantity from the POST data, default to 1

    if new_quantity < 1:
        messages.error(request, "Quantity must be at least 1.")
        return redirect('cart_items')

    if request.user.is_authenticated:
        # Update the cart item for the logged-in user
        cart_item = CartItem.objects.filter(user=request.user, Book_id=book_id).first()
    else:
        # Update the cart item for the session-based user
        session_key = request.session.session_key
        if not session_key:
            messages.error(request, "Session not found.")
            return redirect('cart_items')

        cart_item = CartItem.objects.filter(session_key=session_key, Book_id=book_id).first()

    if cart_item:
        cart_item.quantity = new_quantity
        cart_item.save()
        messages.success(request, "Cart item updated successfully!")
    else:
        messages.error(request, "Cart item not found.")

    return redirect('cart_items')


def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already taken", extra_tags="register")
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                messages.success(request, "Account created successfully!" , extra_tags="register")
                return redirect('login')
        else:
            messages.error(request, "Passwords do not match", extra_tags="register")

    return render(request, 'user/register.html')



def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            session_key = request.session.session_key  # Get the session key before login
            login(request, user)  # Log the user in

            # Transfer session-based cart items to the logged-in user
            CartItem.objects.filter(session_key=session_key, user=None).update(user=user, session_key=None)

            messages.success(request, "Login successful!",extra_tags="login")
            return redirect('index')  # Change 'home' to your actual home page

        else:
            messages.error(request, "Invalid username or password", extra_tags="login")

    return render(request, 'user/login.html')

def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out")
    return redirect('login')



@require_POST
def checkout(request):
    """
    Handles the checkout process for authenticated users and generates a QR code for payment.
    """
    if not request.user.is_authenticated:
        messages.error(request, "You need to log in to check out.")
        return redirect('login')

    # Fetch cart items for the logged-in user
    cart_items = CartItem.objects.filter(user=request.user)

    if not cart_items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect('cart_items')

    # Calculate total price
    total_price = sum(item.Book.price * item.quantity for item in cart_items)
    total_price = f"{total_price:.2f}"  # Convert to a string with 2 decimal places

    # Create an order
    order = Order.objects.create(
        user=request.user,
        total_price=total_price,
    )

    # Create order items
    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            book=item.Book,
            quantity=item.quantity,
            price=item.Book.price,
        )


    bill_number = f"INV{order.id}"  # Use the order ID as the bill number
    

    # Generate KHQR String for payment
    khqr = KHQR("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7ImlkIjoiNzAzMTA5OWJiZWI5NDRkYyJ9LCJpYXQiOjE3NDM2MDYzMjcsImV4cCI6MTc1MTM4MjMyN30.aEzseGAUdX8PcIFxj2a5xN0QzeF-ZwL-tIHU2t_iv_Y")  # Replace with your actual Bakong Developer Token
    khqr_string = khqr.create_qr(
        bank_account='vuth_chanchesda@aclb',  # Your Bakong account ID
        merchant_name='CHANCHESDA VUTH',
        merchant_city='PHNOM PENH',
        amount=total_price,  # Set the total price as the amount
        currency='USD',
        store_label='Book Shop',
        phone_number='070482285',
        bill_number=bill_number,  # Use the order ID as the bill number
        terminal_label='Cashier_1',
        static=False  # Set to True for a static QR code
    )

    # Compute the MD5 hash of the KHQR string
    md5_hash = khqr.generate_md5(khqr_string)

    print("Calling khqr.check_payment...")
    payment_status = khqr.check_payment(md5_hash)
    print("Payment Status:", payment_status)
    print("MD5 Hash:", md5_hash)
    print("Generated KHQR String:", khqr_string)

    testmd5 = hashlib.md5(khqr_string.encode()).hexdigest()
    print("MD5 test:", testmd5)


    # Save the MD5 hash in the order (optional)
    order.md5_hash = md5_hash
    order.save()

    # Generate QR Code Image
    qr = qrcode.make(khqr_string)
    qr_buffer = BytesIO()
    qr.save(qr_buffer, format="PNG")
    qr_base64 = base64.b64encode(qr_buffer.getvalue()).decode()

    # Render the payment page with the QR code and MD5 hash
    return render(request, 'accounts/payment.html', {
        'qr_code_url': f"data:image/png;base64,{qr_base64}",
        'qr_data': khqr_string,
        'md5_hash': md5_hash,
        'total_price': total_price,
    })


def verify_payment(request, md5_hash):
    """
    Verifies the payment status using the Bakong API.
    """
    try:
        # Bakong API endpoint
        url = "https://api-bakong.nbc.gov.kh/v1/check_transaction_by_md5"
        headers = {
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7ImlkIjoiNzAzMTA5OWJiZWI5NDRkYyJ9LCJpYXQiOjE3NDM2MDYzMjcsImV4cCI6MTc1MTM4MjMyN30.aEzseGAUdX8PcIFxj2a5xN0QzeF-ZwL-tIHU2t_iv_Y",  # Replace with your actual API token
            "Content-Type": "application/json",
        }
        payload = {"md5": md5_hash}

        # Send a POST request to the Bakong API
        response = requests.post(url, json=payload, headers=headers)
        print("Bakong API Response:", response.status_code, response.text)
        print("MD5 Hash for Verification:", payload)

        if response.status_code == 200:
            payment_status = response.json()

            # Check if the transaction is found
            if payment_status.get("responseCode") == 1:  # Transaction not found
                return JsonResponse({"error": "Transaction not found. Please complete the payment."}, status=404)

            # If the payment is completed, update the order status
            if payment_status.get("responseCode") == 0:  # Payment successful
                try:
                    order = Order.objects.get(md5_hash=md5_hash)
                    order.status = "Completed"
                    order.save()

                    # Clear the cart for the user
                    if request.user.is_authenticated:
                        CartItem.objects.filter(user=request.user).delete()
                    else:
                        session_key = request.session.session_key
                        if session_key:
                            CartItem.objects.filter(session_key=session_key).delete()
                

                except Order.DoesNotExist:
                    return JsonResponse({"error": "Order not found"}, status=404)

                  # Return a JSON response with payment status, redirect URL, and message
                                # Return the payment status as a JSON response
                return JsonResponse(payment_status, status=200)

           
            else:
                return JsonResponse({"error": "Payment verification failed."}, status=400)
        else:
            return JsonResponse({"error": response.text}, status=response.status_code)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)