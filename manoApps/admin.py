from django.contrib import admin
from .models import Asmenys


# @admin.action(description='make public')
# def make_published(queryset):
#     queryset.update(genre='Adventure')


class AsmenysAdmin(admin.ModelAdmin):
    list_display = ['user_name', 'user_surname', 'user_birth_date', 'user_age']
    # ordering = ['user_name']
    # actions = [make_published]


admin.site.register(Asmenys, AsmenysAdmin)
