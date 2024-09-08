from django.contrib import admin
from .models import Company, Favorite, Preference, CompanyNote, PlaceOfWork

@admin.register(PlaceOfWork)
class PlaceOfWorkAdmin(admin.ModelAdmin):
    list_display = ('place',)

class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'company', 'created_at')

class PreferenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'company', 'preference_level')

class CompanyNoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'company', 'note', 'created_at', 'updated_at')

admin.site.register(Company)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Preference, PreferenceAdmin)
admin.site.register(CompanyNote, CompanyNoteAdmin)
