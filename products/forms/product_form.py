from django import forms
from products.models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        labels = {
            "brand": "Бренд",
            "model": "Модель",
            "year": "Рік",
            "available": "Доступний",
            "consumption": "Витрата пального",
            "color": "Колір",
            "description": "Опис",
            "price": "Ціна",
            "stock": "Кількість",
            "image": "Зображення"
        }
