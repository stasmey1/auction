from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import CreateView, DeleteView

from .models import Category, Auction, Order
from .forms import CategoryForm, AuctionForm, OrderForm


def index(request):
    category_list = Category.objects.all()
    return render(request, 'core\\home_page.html', locals())


def category(request, pk):
    category = Category.objects.get(pk=pk)
    return render(request, 'core\\category\\category.html', locals())


class CreateCategoryView(CreateView):
    template_name = 'core\\forms\\create_form.html'
    model = Category
    form_class = CategoryForm


def order(request, pk):
    order = Order.objects.get(pk=pk)
    return render(request, 'core\\order\\order.html', locals())


class CreateOrderView(CreateView):
    template_name = 'core\\forms\\create_form.html'
    model = Order
    form_class = OrderForm


def auction(request, pk):
    auction = Auction.objects.get(pk=pk)
    return render(request, 'core\\auction\\auction.html', locals())


class CreateAuctionView(CreateView):
    template_name = 'core\\forms\\create_form.html'
    model = Auction
    form_class = AuctionForm


class DeleteAuctionView(DeleteView):
    template_name = 'core\\forms\\delete_form.html'
    model = Auction


def start(request, pk):
    auction = Auction.objects.get(pk=pk)
    auction.start_auction()
    return redirect('auction', auction.pk)


def stop(request, pk):
    auction = Auction.objects.get(pk=pk)
    auction.stop()
    return redirect('auction', auction.pk)
