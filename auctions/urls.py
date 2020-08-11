from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("add/<str:title>", views.addwatchlist, name="addwatchlist"),
    path("remove/<str:title>", views.removewatchlist, name="removewatchlist"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:cat>", views.category, name="category"),
    path("bid/<str:title>", views.bid, name="bid"),
    path("comment/<str:title>", views.comment, name="comments"),
    path("<str:title>", views.item, name="item")
]
