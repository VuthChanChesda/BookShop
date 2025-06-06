from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User


# Create your models here.

class Author(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True)
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Publisher(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)  # Number of books available
    description = models.TextField(blank=True, null=True)
    cover_image = models.CharField(max_length=200)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    publication_date = models.DateField(blank=True, null=True)
    language = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True)
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Reviewer(models.Model):
    name = models.CharField(max_length=100)
    # email = models.EmailField()

    def __str__(self):
        return self.name
    
class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    comment = models.TextField(blank=True, null=True)
    reviewer = models.ForeignKey(Reviewer, on_delete=models.CASCADE, default=1)  # Assuming reviewer with ID 1 exists

    def __str__(self):
        return self.comment

class CartItem(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Associate with user
    Book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    session_key = models.CharField(max_length=40, null=True, blank=True) 
    
    def __str__(self):
        return self.Book.title


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Only authenticated users can place orders
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Pending')  # e.g., Pending, Completed, Canceled
    md5_hash = models.CharField(max_length=32, blank=True, null=True)  # Store the MD5 hash


    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price at the time of purchase

    def __str__(self):
        return f"{self.book.title} (x{self.quantity})"


