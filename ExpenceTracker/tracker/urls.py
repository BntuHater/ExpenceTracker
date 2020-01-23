from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

from . import views


urlpatterns = [
    path('', views.home, name='tracker-home'),
    path('about/', views.about, name='tracker-about'),
    path('register/', views.registration, name='register'),
    path('profile/', views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='tracker/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='tracker/logout.html'), name='logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='tracker/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='tracker/password_reset_done.html'),
        name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(template_name='tracker/password_reset_confirm.html'),
        name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='tracker/password_reset_complete.html'),
        name='password_reset_complete'),
]


urlpatterns += [
    path('categories/', views.CategoryListView.as_view(), name='categories'),
    path('categories/new/', views.CategoryCreateView.as_view(), name='category-create'),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view(), name='category-detail'),
    path('categories/<int:pk>/update/', views.CategoryUpdateView.as_view(), name='category-update'),
    path('categories/<int:pk>/delete/', views.CategoryDeleteView.as_view(), name='category-delete'),
]

urlpatterns += [
    path('products/', views.ProductListView.as_view(), name='products'),
    path('products/new/', views.ProductCreateView.as_view(), name='product-create'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('products/<int:pk>/update/', views.ProductUpdateView.as_view(), name='product-update'),
    path('products/<int:pk>/delete/', views.ProductDeleteView.as_view(), name='product-delete'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)