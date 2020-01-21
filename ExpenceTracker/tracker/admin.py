from django.contrib import admin
from .models import User, Profile, Category, Product

admin.site.register(Profile)
admin.site.register(Category)
admin.site.register(Product)
