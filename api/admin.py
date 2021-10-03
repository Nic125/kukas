from django.contrib import admin
from api.models import *

admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Expenses)
admin.site.register(Sell)

@admin.register(Product)
class ProductModel (admin.ModelAdmin):
    list_filter = ('name', 'subcategory_id')
    list_display = ('name', 'subcategory_id', 'profit')











