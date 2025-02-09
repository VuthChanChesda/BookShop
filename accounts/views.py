from django.shortcuts import render, get_object_or_404
from .models import Book, Category , Review , CartItem
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json
from django.views.decorators.http import require_GET



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

    # Check if the book is already in the cart
    if CartItem.objects.filter(Book=book, session_key=session_key).exists():
        return JsonResponse({'success': False, 'error': 'Book is already in the cart'})

    # Add or update the cart item
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
    session_key = request.session.session_key
    if not session_key:
        return JsonResponse({'in_cart': False})
    
    in_cart = CartItem.objects.filter(Book_id=book_id, session_key=session_key).exists() #checks if this book is in the cart and ensures it belongs to the current user (.exists() stops searching after finding the first match and returns a boolean value)

    return JsonResponse({'in_cart': in_cart})

@require_GET
def cart_item_count(request):
    session_key = request.session.session_key
    if not session_key:
        return JsonResponse({'count': 0})
    
    count = CartItem.objects.filter(session_key=session_key).count()
    return JsonResponse({'count': count})

def cart_items(request):
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key

    cart_items = CartItem.objects.filter(session_key=session_key)
    total_price = sum(item.Book.price * item.quantity for item in cart_items)
    
    return render(request, 'accounts/cart_items.html', {'cart_items': cart_items, 'total_price': total_price})