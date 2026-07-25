from django.contrib import admin
from django.core.mail import send_mail
from django.conf import settings


from .models import Dokiman, EnstriksyonPeman, NivoKou, AkseEtidyan, PrevPeman, Tes, VerifikasyonEmail
from .models import LesonKou
from .models import Devwa , Setifika
admin.site.register(Setifika)


@admin.register(AkseEtidyan)
class AkseEtidyanAdmin(admin.ModelAdmin):
    list_display = ('etidyan', 'gen_akse')
    list_filter = ('gen_akse',)
    search_fields = ('etidyan__email', 'etidyan__first_name', 'etidyan__last_name')

    def save_model(self, request, obj, form, change):
        # Si nou nan yon modifikasyon (change) epi ti kaz 'gen_akse' a tounen True (debloque)
        if change and 'gen_akse' in form.changed_data and obj.gen_akse:
            suje = "Aksè ou Debloke! - Elite English Academy"
            mesaj = (
                f"Felisitasyon {obj.etidyan.first_name}!\n\n"
                f"Peman ou an valide ak siksè. Aksè ou sou platfòm Elite English Academy an debloke kounye a.\n\n"
                f"Ou ka konekte ak imèl ou ({obj.etidyan.email}) ak modpas ou te chwazi lè w t ap enskri a pou w ka swiv kou yo.\n\n"
                f"Bòn chans!"
            )
            
            try:
                send_mail(suje, mesaj, settings.DEFAULT_FROM_EMAIL, [obj.etidyan.email])
            except Exception as e:
                pass  # Si imèl la pa ka voye, sa pa anpeche admin lan sove aksè a

        super().save_model(request, obj, form, change)


@admin.register(PrevPeman)
class PrevPemanAdmin(admin.ModelAdmin):
    list_display = ('user', 'metod_peman', 'nimewo_tranzaksyon', 'date_voye', 'valide')
    list_filter = ('metod_peman', 'valide')
    search_fields = ('user__email', 'nimewo_tranzaksyon')


@admin.register(VerifikasyonEmail)
class VerifikasyonEmailAdmin(admin.ModelAdmin):
    list_display = ('user', 'kod', 'estati_verifye')
    search_fields = ('user__email', 'kod')
@admin.register(LesonKou)
class LesonAdmin(admin.ModelAdmin):
    list_display = ('tit', 'fichye_odyo', 'fichye_videyo', 'lyen_videyo')
    search_fields = ('tit',)    

@admin.register(EnstriksyonPeman)
class EnstriksyonPemanAdmin(admin.ModelAdmin):
    list_display = ('nimewo_moncash', 'nimewo_natcash')
admin.site.register(NivoKou)

@admin.register(Dokiman)
class DokimanAdmin(admin.ModelAdmin):
    list_display = ('tit', 'date_kreye')

@admin.register(Devwa)
class DevwaAdmin(admin.ModelAdmin):
    list_display = ('tit', 'date_limit')
    # Sa ede nan fòm admin lan pou l ranje pyès yo byen pwòp
    fieldsets = (
        ("Enfòmasyon Prensipal", {
            'fields': ('tit', 'konsiy', 'date_limit')
        }),
        ("Fichye oswa Mèdyal pou Devwa a (Chwazi sa w bezwen an)", {
            'fields': ('fichye_dokiman', 'fichye_odyo', 'lyen_videyo', 'fichye_videyo')
        }),
    )
@admin.register(Tes)
class TesAdmin(admin.ModelAdmin):
    list_display = ('tit', 'duree_minit')   
