from django.contrib import admin, messages
from .models import Diet, Order
from django.utils.html import format_html


class DietAdmin(admin.ModelAdmin):
    list_display = ["number", "name", "description", "calories", "price_per_day"]
    ordering = ["number", "name"]


admin.site.register(Diet, DietAdmin)


class OrderAdmin(admin.ModelAdmin):
    list_display = ["user_name", "diet", "order_date_from", "order_date_to", "address", "total_price"]


admin.site.register(Order, OrderAdmin)
