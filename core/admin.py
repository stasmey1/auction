from django.contrib import admin
from .models import Auction, Category, Order

admin.site.register(Auction)
admin.site.register(Category)
admin.site.register(Order)
