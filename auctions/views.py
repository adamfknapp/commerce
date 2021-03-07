from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, listing, comment
from .forms import listing_form, comment_form


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
        return render(request, "auctions/view_listing.html", {
            "listing": listing.objects.get(pk =listing_id),
            "comments": comment.objects.filter(listing= listing_id).order_by('-time_create'),
            "comment_form": comment_form
    })

