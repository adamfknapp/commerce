from django.forms import ModelForm
from .models import listing, comment, bid

class listing_form(ModelForm):
    class Meta:
        model = listing
        fields = ["title", "description", "photo", "category", "start_bid"]

class comment_form(ModelForm):
    class Meta:
        model = comment
        fields = ['comment']

class bid_form(ModelForm):
    class Meta:
        model = bid
        fields = ['bid']
