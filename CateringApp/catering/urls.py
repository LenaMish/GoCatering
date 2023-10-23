from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    path("register", views.RegisterView.as_view(), name="register"),
    path("login", views.LoginView.as_view(), name="login"),
    path("logout", views.LogoutView.as_view(), name="logout"),
    path("", views.DietsView.as_view(), name="diets"),
    path("diet/int:<pk>", views.DietDetailsView.as_view(), name="diets_details"),
    path('orders', views.OrdersView.as_view(), name='orders'),
    path('make_order/<int:pk>', views.MakeOrderView.as_view(), name='make_order'),
    path('order_preview/<int:pk>', views.OrderPreviewView.as_view(), name='order_preview'),
    path('confirm_order/<int:pk>', views.OrderConfirmView.as_view(), name='confirm_order'),
    path("activate/<code>", views.ActivateAccountView.as_view(), name="activate"),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
