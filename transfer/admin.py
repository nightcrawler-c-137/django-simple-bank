from django.contrib import admin
from .models import Transfer


class TransferAdmin(admin.ModelAdmin):
    list_display = ('amount', 'transfer_type', 'customer')


admin.site.register(Transfer, TransferAdmin)    