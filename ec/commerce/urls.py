from django.urls import path
from . import views

urlpatterns = [
    path('hm/', views.home, name='home'),
    path('login/', views.login_form, name='login'),
    path('form/', views.form_view, name='form'),
    path('success/', views.success, name='success'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<str:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('confirm-order/', views.confirm_order, name='confirm_order'),
]

