from django.contrib import admin

from .models import Supplier, SupplierCar, SupplierDiscount


admin.site.register(Supplier)
admin.site.register(SupplierCar)
admin.site.register(SupplierDiscount)
