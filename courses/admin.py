from django.contrib import admin
from .models import UserProfile, NivoKou, LesonKou, Devwa, Tes, SoumisyonDevwa
from .models import Profil
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'whatsapp_number', 'level', 'is_paid', 'created_at', 'gen_akse')
    list_filter = ('is_paid', 'level', 'created_at')
    search_fields = ('user__username', 'whatsapp_number')


@admin.register(NivoKou)
class NivoKouAdmin(admin.ModelAdmin):
    list_display = ('nom', 'deskripsyon')


@admin.register(LesonKou)
class LesonKouAdmin(admin.ModelAdmin):
    list_display = ('titre', 'nivo', 'fichye_dokiman', 'fichye_videyo', 'fichye_odyo', 'created_at')
    list_filter = ('nivo',)
    search_fields = ('titre', 'kontni')
@admin.register(Profil)
class ProfilAdmin(admin.ModelAdmin):
    list_display = ('user', 'telephone')
    search_fields = ('user__username', 'telephone')

@admin.register(Devwa)
class DevwaAdmin(admin.ModelAdmin):
    list_display = ('titre', 'leson', 'date_limite')
    fields = ('leson', 'titre', 'deskripsyon', 'fichye_konsiy', 'date_limite')

@admin.register(SoumisyonDevwa)
class SoumisyonDevwaAdmin(admin.ModelAdmin):
    list_display = ('devwa', 'etidyan', 'date_soumisyon', 'note')
    list_editable = ('note',)
    search_fields = ('etidyan__username', 'devwa__titre')
    fields = ('devwa', 'etidyan', 'fichye_repons', 'fichye_or_repons', 'note', 'komante_pwofese')


@admin.register(Tes)
class TesAdmin(admin.ModelAdmin):
    list_display = ('titre',)
