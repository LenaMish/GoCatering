from datetime import timedelta, datetime
from django.utils import timezone
import pytz
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.template.defaultfilters import register
from django.urls import reverse_lazy, reverse
from django.template.loader import render_to_string
import uuid
from django.views import View
from django.views.generic import FormView, CreateView, ListView, DetailView
from rest_framework.views import APIView
from django.http import JsonResponse

from .forms import LoginForm, RegisterForm, OrderDietForm
from .models import Diet, Order, ActivationCode


class RegisterView(CreateView):
    model = User
    template_name = "catering/register.html"
    success_url = reverse_lazy("catering:login")
    form_class = RegisterForm

    def form_valid(self, form):
        form.instance.is_active = False
        result = super().form_valid(form)
        user = form.instance
        activation_code = ActivationCode(user=user, date_expired=datetime.now() + timedelta(minutes=15), code=str(uuid.uuid4()))
        activation_code.save()
        form.instance.user = self.request.user
        messages.add_message(self.request, messages.SUCCESS, 'Thank you for your registration! Check your email to activate your acoount.')
        html_message = render_to_string("catering/welcome_email_message.html",
                                        {"username": user.username, "code": activation_code.code})
        send_mail("Welcome!", "", settings.EMAIL_HOST_USER,
                  [form.cleaned_data["email"]], html_message=html_message)
        return result


class LoginView(FormView):
    template_name = "catering/login.html"
    success_url = reverse_lazy("catering:diets")
    form_class = LoginForm

    def form_valid(self, form):
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            form.add_error("password", "Invalid credentials!")
            return super().form_invalid(form)


class ActivateAccountView(View):
    def get(self, request, code):
        activation_code = ActivationCode.objects.filter(code=code).first()
        now = timezone.now()
        if not activation_code or activation_code.date_expired.timestamp() < datetime.now().timestamp():
            messages.add_message(request, messages.WARNING, "Invalid activate link")
        else:
            activation_code.user.is_active = True
            activation_code.user.save()
            activation_code.delete()
            messages.add_message(request, messages.SUCCESS, "Account activated!")
        return redirect("catering:login")


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("catering:login")


class DietsView(ListView):
    template_name = "catering/diets.html"
    model = Diet
    context_object_name = "diets"


class DietDetailsView(DetailView):
    model = Diet
    template_name = "catering/diets_details.html"
    context_object_name = "diet"


class OrdersView(LoginRequiredMixin, ListView):
    template_name = "catering/orders.html"
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(user_name=self.request.user)


class MakeOrderView(LoginRequiredMixin, FormView):
    template_name = 'catering/make_order.html'
    form_class = OrderDietForm
    success_url = reverse_lazy('catering:order_preview')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        diet_id = self.kwargs['pk']
        context['diet'] = Diet.objects.get(pk=diet_id)
        context['order'] = Order()
        return context


class OrderPreviewView(LoginRequiredMixin, View):
    template_name = 'catering/order_preview.html'

    def post(self, request, pk):
        print(request.POST)

        form = OrderDietForm(request.POST)
        context = {"form": form}

        if form.is_valid():
            diet = Diet.objects.get(id=pk)
            days = (form.cleaned_data["order_date_to"] - form.cleaned_data["order_date_from"]).days
            total_price = diet.price_per_day * days

            context = {
                "diet": diet,
                "date_from": form.cleaned_data["order_date_from"],
                "date_to": form.cleaned_data["order_date_to"],
                "address": form.cleaned_data["address"],
                "total_price": total_price,
                "form": form
            }
        else:
            return redirect("catering:make_order", pk=pk)
        return render(request, self.template_name, context)


class OrderConfirmView(LoginRequiredMixin, View):
    def post(self, request, pk):
        form = OrderDietForm(request.POST)
        if form.is_valid():
            diet = Diet.objects.get(id=pk)
            days = (form.cleaned_data["order_date_to"] - form.cleaned_data["order_date_from"]).days
            total_price = diet.price_per_day * days

            form.instance.diet = diet
            form.instance.total_price = total_price
            form.instance.user_name = request.user
            form.save()

            return redirect("catering:orders")


class DeleteOrderView(View):
    def post(self, request, diet_id):
        orders = Order.objects.filter(diet__id=diet_id)
        if orders.exists():
            orders.first().delete()

        return redirect('catering:orders')


@register.filter
def get_url(url_name):
    return reverse(url_name)


class HomeView(APIView):
    def get(self, request, format=None):
        return JsonResponse({"message":
        'HELLO WORLD FROM DJANGO AND DOCKER'})


