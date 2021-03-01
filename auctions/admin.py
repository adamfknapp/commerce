from django.contrib import admin
from .models import category, listing, bid, comment

# Register your models here.
# per requierment 19
admin.site.register(category)
admin.site.register(listing)
admin.site.register(bid)
admin.site.register(comment)