from django import forms
from .models import Product, Report


class ProductForm(forms.ModelForm):
    # title = forms.CharField(max_length=100)
    # price = forms.DecimalField()
    # image = forms.ImageField()
    class Meta:
        model = Product
        fields = ["name", "price", "image"]


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ["email", "report", "type"]
