from django.contrib import admin

from .models import Campaign, Committee, Contribution

admin.site.register(Campaign)
admin.site.register(Committee)
admin.site.register(Contribution)
