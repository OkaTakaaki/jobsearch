from django.contrib import admin
from .models import Company, Favorite, Preference, CompanyNote

admin.site.register(Company)
admin.site.register(Favorite)
admin.site.register(Preference)
admin.site.register(CompanyNote)
