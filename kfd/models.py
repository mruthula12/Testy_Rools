from atexit import register
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut


class Registration(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    User_role = models.CharField(max_length=20)
    Password = models.CharField(max_length=128)


    def __str__(self):
        return self.user.username


class Product(models.Model):
    product_name = models.CharField(max_length=255)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    photo = models.ImageField(upload_to='product_images/', blank=True, null=True)  # Add this field

    def __str__(self):
        return self.product_name


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=1)

    def save(self, *args, **kwargs):
        # Automatically set product_name from the Product instance if not already set
        if not self.product_name:
            self.product_name = self.product.product_name
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.product_price} ({self.quantity})"

    @property
    def total_price(self):
        return self.product.product_price * self.quantity


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    house_number = models.CharField(max_length=10, null=True, blank=True)
    apartment = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    postal_code = models.CharField(max_length=10, null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)  # For geographic coordinates
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)  # For geographic coordinates
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)


class Supplier_status(models.Model):
    in_out = models.CharField(max_length=200, null=True)
    date_time = models.DateTimeField(auto_now_add=True, null=True)
    supplier_reg = models.ForeignKey(Registration, on_delete=models.CASCADE, related_name='in_status', null=True)
    last_updated = models.DateTimeField(auto_now=True, null=True)

    address = models.CharField(max_length=500, blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)

    def save(self, *args, **kwargs):
        print(f"Saving Supplier_status: {self.latitude}, {self.longitude}, {self.address}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Status for {self.supplier_reg.user.username} on {self.date_time}"


class Checkout(models.Model):
    chekout_reg = models.ForeignKey(
        Registration,
        on_delete=models.CASCADE,
        null=True,
        related_name='checkouts_as_customer'  # Unique reverse accessor for checkout_reg
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    current_address = models.CharField(max_length=150, null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True,blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    quantity = models.IntegerField(default=1, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, null=True)
    added_date = models.DateTimeField(auto_now_add=True, null=True)
    is_approved = models.BooleanField(default=False)
    is_preparing = models.BooleanField(default=False)
    is_prepared = models.BooleanField(default=False)
    is_delivery_partner_arrived = models.BooleanField(default=False)
    is_delivered = models.BooleanField(default=False)
    chk_address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True, related_name='checkout_to_address')

    is_out_of_delivery = models.BooleanField(default=False)
    is_delivered_status = models.BooleanField(default=False)

    # Add related_name to avoid clash for delivery_boy
    delivery_boy = models.ForeignKey(
        Registration,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='checkouts_as_delivery_boy'  # Unique reverse accessor for delivery_boy
    )



    @property
    def total_price(self):
        return self.product.product_price * self.quantity

