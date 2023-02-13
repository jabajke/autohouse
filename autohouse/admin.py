from django.contrib import admin
from .models import (
    Autohouse,
    AutohouseCar,
    AutohouseDiscount,
    AutoHouseSupplierPurchaseHistory
)

admin.site.register(Autohouse)
admin.site.register(AutohouseCar)
admin.site.register(AutohouseDiscount)
admin.site.register(AutoHouseSupplierPurchaseHistory)
