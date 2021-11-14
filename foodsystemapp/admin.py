from django.contrib import admin
from foodsystemapp.models import ResturantLogin, Customerlogin, OrderFood, ResturantDetails, Addfooditems


# Register your models here.

admin.site.register(ResturantLogin)

admin.site.register(Customerlogin)

admin.site.register(OrderFood)

admin.site.register(ResturantDetails)


admin.site.register(Addfooditems)
