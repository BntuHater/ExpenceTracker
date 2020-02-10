from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import Profile, Product

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2',
        ]


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
        ]


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image',]


class DateInput(forms.DateInput):
    input_type = 'date'


class RangedDateInput(forms.Form):
    start = forms.DateField(required=True, widget=DateInput)
    end = forms.DateField(required=True, widget=DateInput)


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        widgets = {'purchase_date': DateInput()}
        fields = [
            'product_name',
            'purchase_date',
            'product_price',
            'category',
        ]
        