from django.contrib import admin
from django.contrib.auth import get_user_model

Customer = get_user_model()


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('email', 'wallet', 'is_staff', 'is_superuser')


admin.site.register(Customer, CustomerAdmin)