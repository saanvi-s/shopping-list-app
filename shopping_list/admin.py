from django.contrib import admin
from .models import Item
from .models import ShoppingList

admin.site.register(Item)
admin.site.register(ShoppingList)

# Register your models here.
