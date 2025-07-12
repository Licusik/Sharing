from django.db import models
from django.contrib.auth.models import User
from django.db import models


class Product(models.Model):
    brand = models.CharField(max_length=50, blank=True, null=True)
    model = models.CharField(max_length=50, blank=True, null=True)
    year = models.PositiveIntegerField(blank=True, null=True)
    available = models.BooleanField(default=True)
    consumption = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    color = models.CharField(max_length=30, blank=True, null=True)

    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(blank=True, null=True, upload_to="products/")

    name = models.CharField(max_length=100, editable=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):

        brand_part = self.brand or ""
        model_part = self.model or ""
        self.name = f"{brand_part} {model_part}".strip()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]

class Booking(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(...)
    email = models.EmailField(...)
    phone = models.CharField(...)
    date_from = models.DateField()
    date_to = models.DateField()


    def __str__(self):
        return f"{self.name} → {self.product} ({self.date_from} — {self.date_to})"
    
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')  
