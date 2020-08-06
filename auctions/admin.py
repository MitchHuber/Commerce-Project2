from django.contrib import admin

from .models import User, Categories, Listings

admin.site.register(User)
admin.site.register(Categories)
admin.site.register(Listings)
