from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


from .models import User, listing, comment
from .forms import listing_form, comment_form, bid_form, active_form


def index(request):
    listings = listing.objects.all()
   
    return render(request, "auctions/index.html", {
                "listings": listings,
            })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def create_listing(request):
    if request.method == "POST":
        form = listing_form(request.POST)

        if form.is_valid():
            listing = form.save(commit=False)
            listing.creator = request.user
            listing.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/error.html", {
                "message": "Something went wrong. listing not created."
            }) 
    else:
        return render(request, "auctions/create_listing.html",{
                "listing_form": listing_form
            })


def view_listing(request, listing_id):
    if request.method == "POST":
       
        # handle a new comment 
        if "new_comment" in request.POST:
            f = comment_form(request.POST)

            if f.is_valid():
                new_comment = f.save(commit=False)
                new_comment.creator = request.user
                new_comment.listing = listing.objects.get(pk =listing_id)
                new_comment.save()
                return HttpResponseRedirect(request.path_info)
            else:
                return render(request, "auctions/error.html", {
                    "message": "Something went wrong. Comment failed."
                }) 

        # handle a new bid
        elif "new_bid" in request.POST:
            f = bid_form(request.POST) 
            submitted_bid = float(f['bid'].value())
            current_price = listing.objects.get(pk =listing_id).get_price()
            
            if f.is_valid() and submitted_bid > current_price:
                new_bid = f.save(commit=False)
                new_bid.bidder = request.user
                new_bid.listing = listing.objects.get(pk =listing_id)
                new_bid.save()   
                return HttpResponseRedirect(request.path_info)
            else:
                return render(request, "auctions/error.html", {
                    "message": "Your bid was not accepted. Please try again."
                })     
        
        # Update is active
        elif "is_active" in request.POST:
            f = active_form(request.POST)
            if f.is_valid():
                obj = f.save(commit=False)
                #MyModel.objects.filter(pk=some_value).update(field1='some value')
                obj.active = listing.objects.filter(pk =listing_id).update(active = False)
                obj.save()
                return HttpResponseRedirect(request.path_info)
            else:
                return render(request, "auctions/error.html", {
                    "message": "Somewthing went wrong. Please try again."
                })     

    else:
        return render(request, "auctions/view_listing.html", {
            "listing": listing.objects.get(pk =listing_id),
            "comments": comment.objects.filter(listing= listing_id).order_by('-time_create'),
            "comment_form": comment_form,
            "bid_form": bid_form,
            "active_form": active_form
        })

