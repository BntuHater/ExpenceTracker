from django.db import models
from django.contrib.auth.models import User

from datetime import date


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return self.user.username


class Category(models.Model):
    category_type = models.CharField(max_length=100, verbose_name='Product category')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    

    def __str__(self):
        return self.category_type


class Product(models.Model):
    product_name = models.CharField(max_length=100, verbose_name='Product name')
    purchase_date = models.DateField(default=date.today, blank=True, verbose_name='Date of purchase')
    product_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Product price')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.product_name} : {self.purchase_date} : {self.product_price}'