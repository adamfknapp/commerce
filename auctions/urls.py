from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("listings/<str:isactive>/", views.listings, name="listings"),
    path("view_listing/<str:listing_id>/", views.view_listing, name="view_listing"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
]
