from django.urls import path, include
from . import views  # Import the views module

urlpatterns = [
    # Index and Search
    path('', views.index, name='index'),
    path('search/', views.search, name='search'),
    path('api/search/', views.search_books, name='search_books'),



    # Authentication
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    

    #payment
    path('checkout/', views.checkout, name='checkout'),
    path('verify-payment/<str:md5_hash>/', views.verify_payment, name='verify_payment'),

    path('history/items/', views.completed_order_items, name='completed_order_items'),

    # Cart-related URLs
    path('cart/items/', views.cart_items, name='cart_items'),
    path('cart/item_count/', views.cart_item_count, name='cart_item_count'),
    path('cart/delete/<int:book_id>/', views.delete_cart_item, name='delete_cart_item'),
    path('cart/update/<int:book_id>/', views.update_cart_item, name='update_cart_item'),
    path('books/add_to_cart/<int:book_id>/', views.add_to_cart, name='add_to_cart'),
    path('books/is_in_cart/<int:book_id>/', views.is_in_cart, name='is_in_cart'),

    # Book-related URLs
    path('books/<slug:slug>/', views.book_detail, name='book_detail'),
    path('books/category/new/', views.new_books, name='new_books'),
    path('books/category/<slug:slug>/', views.show_by_category, name='book_by_category'),
]