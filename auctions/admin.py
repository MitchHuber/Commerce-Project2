from django.contrib import admin

from .models import User, Categories, Listings, Watchlist, Bids, Comments, ListingsWon

admin.site.register(User)
admin.site.register(Categories)
admin.site.register(Listings)
admin.site.register(Watchlist)
admin.site.register(Bids)
admin.site.register(Comments)
admin.site.register(ListingsWon)
