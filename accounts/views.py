from django.shortcuts import render, get_object_or_404
from .models import Book, Category , Review
from django.http import JsonResponse



# Create your views here.

def home(request):
    return render(request, 'accounts/home.html')




# def coffee_list(request):
#     books = Book.objects.all()  # Query the database for all customers
#     context = {
#         'books': books
#     }
#     return render(request, 'accounts/coffee.html', books)



def index(request):
    # Get the category by name or raise a 404 error if not found
    category_name = 'Comics & Graphic Novels'
    category = get_object_or_404(Category, name=category_name)

    category_manga= 'Manga & Graphic Novels'
    category_manga_list = get_object_or_404(Category, name=category_manga)

    category_horror = 'Horror'
    category_horror_list = get_object_or_404(Category, name=category_horror)
    
    # Filter books by the given category
    books = Book.objects.filter(category=category)
    books_manga = Book.objects.filter(category=category_manga_list)
    books_horror = Book.objects.filter(category=category_horror_list)

    
    context = {
        'category': category,
        'books': books,
        'books_manga': books_manga,
        'books_horror': books_horror,   
    }
    
    return render(request, 'accounts/home.html', context)


def book_detail(request, slug):
    book = get_object_or_404(Book, slug=slug)
    reviews = Review.objects.filter(book=book)

     # Get the category by name or raise a 404 error if not found
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
    # query = request.GET.get('q', '')
    # books = Book.objects.filter(title__icontains=query) if query else []
    # context = {
    #     'query': query,
    #     'books': books,
    # }
    return render(request, 'accounts/search.html')  

def search_books(request):
    query = request.GET.get('q', '')
    if query:
        books = Book.objects.filter(title__icontains=query) #perform case-insensitive search on title
        results = []
        for book in books:
            results.append({
                'title': book.title,
                'author': book.author.name,
                'price': book.price,
                'cover_image': book.cover_image,
                'slug': book.slug,
            })
        return JsonResponse(results, safe=False)
    return JsonResponse([], safe=False)

def new_books(request):
   

    books = Book.objects.all().order_by('-id')  # Order by primary key in descending order
    context = {
        'books': books
    }
    return render(request, 'accounts/show_by_category.html', context)

