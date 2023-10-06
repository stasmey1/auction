from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('category/<int:pk>/', views.category, name='category'),
    path('create_category/', views.CreateCategoryView.as_view(), name='create_category'),

    path('order/<int:pk>/', views.order, name='order'),
    path('create_order/', views.CreateOrderView.as_view(), name='create_order'),

    path('auction/<int:pk>/', views.auction, name='auction'),
    path('create_auction/', views.CreateAuctionView.as_view(), name='create_auction'),
    path('delete_auction/<int:pk>/', views.DeleteAuctionView.as_view(), name='delete_auction'),

    path('start/<int:pk>/', views.start, name='start'),
    path('stop/<int:pk>/', views.stop, name='stop'),

]
