from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class category(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return f"{self.name}"


class listing(models.Model):
    title = models.CharField(max_length=20, unique=False)
    description = models.TextField(max_length=5000, default="no description")
    creator = models.ForeignKey(User, on_delete=models.CASCADE,
                                related_name="listings")
    photo = models.URLField(max_length=200, blank=True, null=True)
    category = models.ForeignKey(category, on_delete=models.CASCADE,
                                 related_name="listings", default="None")
    start_bid = models.DecimalField(max_digits=5, decimal_places=0, default=1)
    time_create = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)  # requierment 15

    def num_bids(self):
        """
        caluclate the number of bids on the listing
        """
        return len(list(self.bids.all()))

    def high_bidder(self):
        """
        deterine the current high bidder
        """
        for bid in self.bids.order_by('-bid')[:1]:
            return bid.bidder

    def get_price(self):
        """
        get current price per requierment 8
        sort bids in decending order of price and select 1st record
        ensure current bid >= staring bid. Set current price before loop
        in case no bids exist.
        """
        current_price = self.start_bid
        for bid in self.bids.order_by('-bid')[:1]:
            current_price = max(bid.bid, current_price)
        return current_price

    def __str__(self):
        return f"title: {self.title} | category: {self.category}"


class bid(models.Model):
    time_create = models.DateTimeField(auto_now_add=True)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="bids")
    listing = models.ForeignKey(listing, on_delete=models.CASCADE,
                                related_name="bids")
    bid = models.DecimalField(max_digits=5, decimal_places=0, default=1)

    def __str__(self):
        return f"listing: {self.listing} | bid: {self.bid}"


class comment(models.Model):
    time_create = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE,
                                related_name="comments")
    listing = models.ForeignKey(listing, on_delete=models.CASCADE,
                                related_name="comments")
    comment = models.CharField(max_length=100)

    def __str__(self):
        return f"listing: {self.listing} | bid: {self.comment}"
