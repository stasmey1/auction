from django.forms import ModelForm
from .models import Category, Auction, Order


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = '__all__'


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'


class AuctionForm(ModelForm):
    class Meta:
        model = Auction
        fields = ('is_increase_mode',
                  'is_protected_mode',
                  'min_price',
                  'max_price',
                  'step_price',
                  'interval',
                  'order_id',
                  'client_id',
                  )
