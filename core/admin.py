from django.contrib import admin
from django.utils.html import format_html
from .models import Evenement, Temoignage, Video, SliderImage, CarousselImage, UtilisateurEtendu

class SliderImageAdmin(admin.ModelAdmin):
    list_display = ('titre', 'sous_titre', 'ordre', 'actif', 'apercu_image')
    list_editable = ('ordre', 'actif')
    list_filter = ('actif', 'date_ajout')
    search_fields = ('titre', 'sous_titre')
    ordering = ('ordre', '-date_ajout')
    
    def apercu_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 100px;" />', obj.image.url)
        return "Pas d'image"
    apercu_image.short_description = 'Aperçu'

class CarousselImageAdmin(admin.ModelAdmin):
    list_display = ('titre', 'date_ajout', 'apercu_image')
    list_filter = ('date_ajout',)
    search_fields = ('titre',)
    
    def apercu_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 100px;" />', obj.image.url)
        return "Pas d'image"
    apercu_image.short_description = 'Aperçu'

admin.site.register(Evenement)
admin.site.register(Temoignage)
admin.site.register(Video)
admin.site.register(UtilisateurEtendu)
admin.site.register(SliderImage, SliderImageAdmin)
admin.site.register(CarousselImage, CarousselImageAdmin)

