from django.db import models

class Order(models.Model):
    customer = models.CharField(max_length=100)
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('shipped', 'Shipped')])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.customer}"

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    is_published = models.BooleanField(default=False)
    published_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title
