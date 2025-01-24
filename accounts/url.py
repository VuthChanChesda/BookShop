from django.urls import path, include
from . import views  # Import the views module

urlpatterns = [
    
    path('search/', views.search, name='search'),
    path('books/category/new/', views.new_books, name='new_books'),
    path('api/search/', views.search_books, name='search_books'),
    path('' , views.index, name='index'),
    path('books/<slug:slug>/', views.book_detail, name='book_detail'),
    path('books/category/<slug:slug>/', views.show_by_category, name='book_by_category'),


]