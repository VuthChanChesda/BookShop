from django.contrib import admin
from .models import Author, Category, Book, Reviewer, Review , Publisher , CartItem , Order , OrderItem

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'price', 'stock', 'publisher', 'publication_date', 'language')
    list_filter = ('author', 'category', 'publisher', 'publication_date', 'language')
    search_fields = ('title', 'author__name', 'category__name', 'publisher', 'publication_date', 'language')

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('book', 'comment' , 'reviewer')
    list_filter = ('book',)
    search_fields = ('book__title', 'comment')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_price', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'status')
    ordering = ('-created_at',)

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'book', 'quantity', 'price')
    search_fields = ('order__id', 'book__title')
    ordering = ('order',)

# Register your models here.
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Book, BookAdmin)  # Register Book with BookAdmin
admin.site.register(Reviewer)
admin.site.register(Review, ReviewAdmin)  # Register Review with ReviewAdmin
admin.site.register(Publisher)
admin.site.register(CartItem)

