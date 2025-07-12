from django import forms
from products.models import Product


class EditProduct(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter name"}),
            "category": forms.Select(attrs={"class": "form-control"}),
        }
