from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.db import models


class Product(models.Model):
    id = models.AutoField(
        db_index=True,
        primary_key=True,
        validators=[
            MinLengthValidator(12),
            MaxLengthValidator(12),
        ],
        unique=True,
        editable=True,
        blank=True,
        null=False,
        default=None,
        verbose_name="ID",
        max_length=12,
    )
    name = models.CharField(
        db_index=False,
        primary_key=False,
        unique=False,
        editable=True,
        blank=True,
        null=False,
        default="",
        verbose_name="Name",
        max_length=200,
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=False,
        default=0.0,
        verbose_name="Price",
    )
    image = models.FileField(upload_to="static/src/products")
    status = models.BooleanField(
        null=False,
        default=True,
        verbose_name="Availability",
    )

    class Meta:
        app_label = "django_app"
        ordering = ("status", "-price")
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        if self.status:
            status = "In stock"
        else:
            status = "Out of stock"
        return f"<Product [{self.id}] {self.name} {self.price} | {status}>"


class Report(models.Model):
    id = models.AutoField(
        db_index=True,
        primary_key=True,
        validators=[
            MinLengthValidator(12),
            MaxLengthValidator(12),
        ],
        unique=True,
        editable=True,
        blank=True,
        null=False,
        default=None,
        verbose_name="ID",
        max_length=12,
    )
    email = models.CharField(
        db_index=False,
        primary_key=False,
        unique=False,
        editable=True,
        blank=True,
        null=False,
        default="",
        verbose_name="Email",
        max_length=200,
    )
    report = models.CharField(
        db_index=False,
        primary_key=False,
        unique=False,
        editable=True,
        blank=True,
        null=False,
        default="",
        verbose_name="Report",
        max_length=200,
    )
    type = models.CharField(
        db_index=False,
        primary_key=False,
        unique=False,
        editable=True,
        blank=True,
        null=False,
        default="",
        verbose_name="Type",
        max_length=50,
    )
    date = models.CharField(
        db_index=False,
        primary_key=False,
        unique=False,
        editable=True,
        blank=True,
        null=True,
        default="",
        verbose_name="Date",
        max_length=50,
    )
    status = models.BooleanField(
        null=False,
        default=True,
        verbose_name="Status",
    )

    class Meta:
        app_label = "django_app"
        ordering = ("status", "id", "date")
        verbose_name = "Report"
        verbose_name_plural = "Reports"

    def __str__(self):
        if self.status:
            status = "Active"
        else:
            status = "Inactive"
        return f"<Report [{self.id}] {self.email} {self.type} | {status}>"
