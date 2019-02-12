from django.contrib import admin

from .models import Politician, Campaign

admin.site.register(Politician)
admin.site.register(Campaign)