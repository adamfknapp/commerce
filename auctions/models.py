from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class category(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return f"{self.name}"


class listing(models.Model):
    title = models.CharField(max_length=20)
    description = models.TextField(max_length=5000, default="no description")
    creator = models.CharField(max_length=10, unique=True, default="default_user")
    photo = models.URLField(max_length=200, blank=True, null=True)
    category = models.ForeignKey(category, on_delete=models.CASCADE,
                                 related_name="listings", default="None")
    start_bid = models.DecimalField(max_digits=5, decimal_places=0, default=1)
    time_create = models.DateTimeField(auto_now_add=True)
    active_time = models.IntegerField(default=1)  # in hours
    close_early = models.BooleanField(default=False)  # requierment 15

    def __str__(self):
        return f"title: {self.title} | is active: {self.isactive}"


class bid(models.Model):
    time_create = models.DateTimeField(auto_now_add=True)
    # bidder = request.user
    listing = models.ForeignKey(listing, on_delete=models.CASCADE,
                                related_name="bids")
    bid = models.DecimalField(max_digits=5, decimal_places=0, default=1)

    def __str__(self):
        return f"listing: {self.listing} | bid: {self.bid}"


class comment(models.Model):
    time_create = models.DateTimeField(auto_now_add=True)
    # bidder = request.user
    listing = models.ForeignKey(listing, on_delete=models.CASCADE,
                                related_name="comments")
    comment = models.CharField(max_length=100)

    def __str__(self):
        return f"listing: {self.listing} | bid: {self.comment}"
