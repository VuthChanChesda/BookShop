from django.urls import path, include
from . import views  # Import the views module

urlpatterns = [

    path('', views.index, name='index'),
    path('search/', views.search, name='search'),
    path('books/category/new/', views.new_books, name='new_books'),
    path('books/add_to_cart/<int:book_id>/', views.add_to_cart, name='add_to_cart'),
    path('api/search/', views.search_books, name='search_books'),
    path('books/<slug:slug>/', views.book_detail, name='book_detail'),
    path('books/category/<slug:slug>/', views.show_by_category, name='book_by_category'),
    path('books/is_in_cart/<int:book_id>/', views.is_in_cart, name='is_in_cart'),
    path('cart/item_count/', views.cart_item_count, name='cart_item_count'),




]