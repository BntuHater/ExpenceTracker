from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.db import transaction
from django.urls import reverse_lazy
from django.forms import inlineformset_factory
from django.template.loader import get_template
# from django.contrib.sites.shortcuts import get_current_site
# from django.utils.encoding import force_bytes, force_text
# from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
# from django.template.loader import render_to_string
# from django.core.mail import EmailMessage

# from .tokens import account_activation_token
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, ProductForm, DateInput, RangedDateInput
from .models import Category, Product
from .calculate import calc_all_time_stats, calc_current_month_stats, calc_previous_month_stats, calc_ranged_stats


@login_required
def get_all_time_stats(request):
    stats_dict = 0
    total_expences = 1
    products = Product.objects.filter(user=request.user)
    all_time_stats = calc_all_time_stats(products)
    context = {
        'all_time_stats': all_time_stats[stats_dict],
        'total': all_time_stats[total_expences],
    }
    return render(request, 'tracker/all_time_stats.html', context)


@login_required
def get_current_month_stats(request):
    stats_dict = 0
    total_expences = 1
    products = Product.objects.filter(user=request.user)
    current_month_stats = calc_current_month_stats(products)
    context = {
        'current_month_stats': current_month_stats[stats_dict],
        'total': current_month_stats[total_expences],
    }
    return render(request, 'tracker/current_month_stats.html', context)


@login_required
def get_previous_month_stats(request):
    stats_dict = 0
    total_expences = 1
    products = Product.objects.filter(user=request.user)
    previous_month_stats = calc_previous_month_stats(products)
    context = {
        'previous_month_stats': previous_month_stats[stats_dict],
        'total': previous_month_stats[total_expences],
    }
    return render(request, 'tracker/previous_month_stats.html', context)


@login_required
def get_ranged_stats(request):
    stats_dict = 0
    total_expences = 1
    form = RangedDateInput(request.GET)
    if form.is_valid():
        products = Product.objects.filter(user=request.user)
        start = form.cleaned_data['start']
        end = form.cleaned_data['end']
        ranged_stats = calc_ranged_stats(products, start, end)
        context = {
            'start': start,
            'end': end,
            'ranged_stats': ranged_stats[stats_dict],
            'total': ranged_stats[total_expences],
        }
        return render(request, 'tracker/ranged_stats.html', context)
    else:
       range_form = RangedDateInput()
    return render(request, 'tracker/date_range.html', {'form': range_form})


@login_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.save()
            return redirect('product-detail', pk=product.pk)
    else:
        form = ProductForm()
    return render(request, 'tracker/product_form.html', {'form': form})


@login_required
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.save()
            return redirect('product-detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)
    return render(request, 'tracker/product_form.html', {'form': form})


def home(request):
    return render(request, 'tracker/base.html')


def about(request):
    return render(request, 'tracker/about.html')


def registration(request):
    if request.method == 'POST':
        form_user = UserRegisterForm(request.POST)
        if form_user.is_valid():
            form_user.save()
            username = form_user.cleaned_data.get('username')
            messages.success(request, f'Your Account Has Been Created')
            return redirect('login')
            # user = form_user.save(commit=False)
            # user.is_active = False
            # user.save()
            # current_site = get_current_site(request)
            # mail_subject = 'Activate your ExpenceTracker account.'
            # message = render_to_string(
            #     'acc_active_email.html',
            #     {
            #         'user': user,
            #         'domain': current_site.domain,
            #         'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            #         'token': account_activation_token.make_token(user),
            #     }
            # )
            # to_email = form.cleaned_data.get('email')
            # email = EmailMessage(mail_subject, massage, to=[to_email])
            # email.send()
            # return HttpResponse('Confirm your email address to complete the registration.')
    else:
        form_user = UserRegisterForm()
    return render(request, 'tracker/register.html', {'form_user': form_user})


# def activate(request, uidb64, token):
#     try:
#         uid = force_text(urlsafe_base64_decode(uidb64))
#         user = User.objects.get(pk=uid)
#     except(TypeError, ValueError, OverflowError, User.DoesNotExist):
#         user = None

#     if user and account_activation_token.check_token(user, token):
#         user.is_active = True
#         user.save()
#         login(request, user)
#         # return redirect('tracker-home')
#         return HttpResponse('Your account has been confirmed.')
#     else:
#         return HttpResponse('Activation link is invalid.')


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your account has been updated')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }

    return render(request, 'tracker/profile.html', context)


class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'tracker/categories.html'
    context_object_name = 'categories'


class CategoryDetailView(LoginRequiredMixin, DetailView):
    model = Category

    def get_success_url(self):
        return reverse_lazy('/')


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    fields = [
        'category_type',
    ]

    # To define user for categories
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('category-detail', kwargs={'pk': self.object.pk})


class CategoryUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Category
    fields = [
        'category_type',
    ]

    def test_func(self):
        category = self.get_object()
        if self.request.user == category.user:
            return True
        return False

    def get_success_url(self):
        return reverse_lazy('category-detail', kwargs={'pk': self.object.pk})


class CategoryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Category

    def test_func(self):
        category = self.get_object()
        if self.request.user == category.user:
            return True
        return False

    def get_success_url(self):
        return reverse_lazy('categories')


class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'tracker/products.html'
    context_object_name = 'products'


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product

    def get_success_url(self):
        return reverse_lazy('/')


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product

    def test_func(self):
        product = self.get_object()
        if self.request.user == product.user:
            return True
        return False

    def get_success_url(self):
        return reverse_lazy('products')