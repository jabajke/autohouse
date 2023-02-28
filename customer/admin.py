from django.contrib import admin

from .models import Customer, CustomerPurchaseHistory, Offer

admin.site.register(Customer)
admin.site.register(Offer)
admin.site.register(CustomerPurchaseHistory)
