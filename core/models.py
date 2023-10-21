import datetime
import threading
import time
from typing import Optional

from django.contrib.auth.models import User
from django.urls import reverse

from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=25)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'pk': self.pk})


class Order(models.Model):
    name = models.CharField(max_length=25)
    info = models.CharField(max_length=225)

    category_id = models.ForeignKey(Category, models.CASCADE, 'orders')
    client_id = models.ForeignKey(User, models.CASCADE, 'client_orders', null=True, blank=True)
    executor_id = models.ForeignKey(User, models.CASCADE, 'executor_orders', null=True, blank=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('order', kwargs={'pk': self.pk})


class Auction(models.Model):
    is_increase_mode = models.BooleanField(blank=True, default=True)
    is_protected_mode = models.BooleanField(blank=True, default=False)
    min_price = models.IntegerField()
    max_price = models.IntegerField()
    total_price = models.IntegerField(null=True, blank=True)
    percentage_reduction = models.IntegerField(null=True, blank=True)

    start_time = models.DateTimeField(auto_now_add=True)
    finish_time = models.DateTimeField(null=True, blank=True)

    step_price = models.IntegerField()
    interval = models.IntegerField(default=8)

    is_winner_exist = models.BooleanField(blank=True, default=False)
    is_step_taken = models.BooleanField(blank=True, default=False)
    is_run = models.BooleanField(blank=True, default=False)
    is_done = models.BooleanField(blank=True, default=False)
    is_stop = models.BooleanField(blank=True, default=False)

    order_id = models.OneToOneField(Order, models.CASCADE)
    client_id = models.ForeignKey(User, models.CASCADE, related_name='client_auction', null=True, blank=True)
    executor_id = models.OneToOneField(User, models.CASCADE, related_name='executor_auction', null=True, blank=True)
    unregister_executor_name = models.CharField(max_length=25, blank=True, null=True)
    unregister_executor_contacts = models.CharField(max_length=225, blank=True, null=True)

    class Meta:
        verbose_name = 'Аукцион'
        verbose_name_plural = 'Аукционы'

    def __str__(self):
        return f'{self.order_id}-auction'

    def get_absolute_url(self):
        return reverse('auction', kwargs={'pk': self.pk})

    def setup_(self) -> None:
        self.total_price = self.min_price
        self.executor_id = None
        self.unregister_executor_name = None
        self.unregister_executor_contacts = None
        self.is_winner_exist = False
        self.is_done = False
        self.is_run = True
        self.is_stop = False
        self.finish_time = None

        self.save()

    def is_can_take_step(self) -> bool:
        return self.total_price + self.step_price <= self.max_price

    def get_percentage_reduction(self) -> int:
        return int((self.total_price / self.min_price) * 100 - 100)

    def auto_price_increase(self) -> None:
        while True:

            if any([self.is_done, self.is_stop]):
                break

            print([i for i in threading.enumerate()])
            print('is_done', self.is_done)
            print('is_stop', self.is_stop)
            print()

            time.sleep(int(self.interval))

            with threading.Lock():
                self.total_price += self.step_price
                self.percentage_reduction = self.get_percentage_reduction()

            self.save()

    def check_for_end(self) -> None:
        while True:

            time.sleep(1)

            if any([self.is_done, self.is_stop]):
                break

            if not self.is_can_take_step():
                with threading.Lock():
                    self.is_done = True
                    self.is_run = False
                    self.finish_time = datetime.datetime.now()

                self.save()

                break

    def save_contacts(self, data: Optional[dict]) -> None:
        if self.is_protected_mode and data:
            self.executor_id = data.get('id')
        else:
            self.unregister_executor_name = data.get('name')
            self.unregister_executor_contacts = data.get('contacts')

        self.save()

    def agree(self, data: Optional[dict] = None) -> None:
        with threading.Lock():
            self.save_contacts(data)
            self.is_winner_exist = True
            self.is_done = True
            self.is_run = False
            self.finish_time = datetime.datetime.now()

        self.save()

    def stop_auction(self) -> None:
        with threading.Lock():
            self.is_run = False
            self.is_stop = True
            self.is_done = True
            self.finish_time = datetime.datetime.now()

        self.save()

    def start_auction(self) -> None:
        self.setup_()
        threading.Thread(name=self.auto_price_increase.__name__, target=self.auto_price_increase).start()
        threading.Thread(name=self.check_for_end.__name__, target=self.check_for_end).start()
