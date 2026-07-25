from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
import random

# 1. Nivo Kou yo (Eg: English Class Level 1 - A1)
class NivoKou(models.Model):
    tit = models.CharField(max_length=200, verbose_name="Tit Nivo a")
    deskripsyon = models.TextField(blank=True, verbose_name="Deskripsyon")

    class Meta:
        verbose_name = "Nivo Kou"
        verbose_name_plural = "Nivo Kou yo"

    def __str__(self):
        return self.tit


class Kou(models.Model):
    nivo = models.ForeignKey(NivoKou, on_delete=models.CASCADE, related_name='kours', verbose_name="Nivo", blank=True, null=True)
    tit = models.CharField(max_length=255, verbose_name="Tit Kou a")
    deskripsyon = models.TextField(blank=True, verbose_name="Deskripsyon")

    class Meta:
        verbose_name = "Kou"
        verbose_name_plural = "Kou yo"

    def __str__(self):
        return self.tit


# 2. Leson yo (Ka yon Videyo oswa yon Odyo)
class LesonKou(models.Model):
    TIP_KONTNI = [
        ('videyo', 'Videyo (Vimeo)'),
        ('odyo', 'Odyo (Audio/Listening)'),
    ]

    nivo = models.ForeignKey(NivoKou, on_delete=models.CASCADE, related_name='leson_yo', verbose_name="Nivo")
    tit = models.CharField(max_length=255, verbose_name="Tit Leson an")
    tip = models.CharField(max_length=10, choices=TIP_KONTNI, default='videyo', verbose_name="Tip Kontni")
    description = models.TextField(blank=True, null=True)
    
    fichye_odyo = models.FileField(upload_to='odyo_leson/', blank=True, null=True, help_text="Upload yon fichye odyo (.mp3, .wav)")
    fichye_videyo = models.FileField(upload_to='videyo_leson/', blank=True, null=True, help_text="Upload yon fichye videyo (.mp4)")
    lyen_videyo = models.URLField(blank=True, null=True, help_text="Oswa kole yon lyen videyo (YouTube, Vimeo, Google Drive, elatriye)")
    dire = models.CharField(max_length=50, verbose_name="Dire a (Eg: 01:50:08 oswa 15:30)")

    class Meta:
        verbose_name = "Leson"
        verbose_name_plural = "Leson yo"

    def __str__(self):
        tip_non = "🎥" if self.tip == 'videyo' else "🎵"
        return f"{tip_non} {self.nivo.tit} - {self.tit}"


# 3. Sistèm kontwòl manyèl pou aktive/dezaktive aksè elèv yo
class AkseEtidyan(models.Model):
    etidyan = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Elèv", related_name="akse")
    gen_akse = models.BooleanField(default=False, verbose_name="Èske li gen aksè nan platfòm lan?")
    not_admin = models.TextField(blank=True, null=True, verbose_name="Nòt sou elèv sa a")

    class Meta:
        verbose_name = "Aksè Elèv"
        verbose_name_plural = "Aksè Elèv yo"

    def __str__(self):
        estati = "AKSIF" if self.gen_akse else "BLOKE"
        return f"{self.etidyan.email} - [{estati}]"


class PrevPeman(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    metod_peman = models.CharField(max_length=50, choices=[
        ('MonCash', 'MonCash'),
        ('Natcash', 'Natcash'),
        ('Zelle', 'Zelle'),
        ('Lòt', 'Lòt')
    ])
    nimewo_tranzaksyon = models.CharField(max_length=100, blank=True, null=True)
    foto_resi = models.ImageField(upload_to='resi_peman/', blank=True, null=True)
    date_voye = models.DateTimeField(auto_now_add=True)
    valide = models.BooleanField(default=False)

    def __str__(self):
        return f"Peman {self.user.username} - {self.metod_peman}"


class VerifikasyonEmail(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    kod = models.CharField(max_length=6)
    estati_verifye = models.BooleanField(default=False)

    def jènere_kod(self):
        self.kod = str(random.randint(100000, 999999))
        self.save()

class EnstriksyonPeman(models.Model):
    nimewo_moncash = models.CharField(max_length=50, blank=True, null=True, help_text="Egzanp: +509 3400-0000")
    nimewo_natcash = models.CharField(max_length=50, blank=True, null=True, help_text="Egzanp: +509 4300-0000")
    enfomasyon_bank = models.TextField(blank=True, null=True, help_text="Egzanp: Unibank: 123-4567-8901 (Non sou kont lan)")
    note_enpotan = models.TextField(blank=True, null=True, help_text="Ti enstriksyon pou etidyan an (egzanp: Antre nimewo tranzaksyon an presizeman)")

    class Meta:
        verbose_name = "Enstriksyon Peman"
        verbose_name_plural = "Enstriksyon Peman yo"

    def __str__(self):
        return "Konfigirasyon Nimewo Peman yo"
class Dokiman(models.Model):
    tit = models.CharField(max_length=200)
    fichye = models.FileField(upload_to='dokiman_kou/')
    description = models.TextField(blank=True, null=True)
    date_kreye = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Dokiman yo"

    def __str__(self):
        return self.tit
class Devwa(models.Model):
    tit = models.CharField(max_length=200)
    konsiy = models.TextField(help_text="Esplike sa eleman yo dwe fè nan devwa sa a")
    
    # Opsyon pou diferan kalite kontni pwofesè a ka met nan devwa a
    fichye_dokiman = models.FileField(upload_to='devwa/dokiman/', blank=True, null=True, help_text="Si se yon PDF/Word")
    fichye_odyo = models.FileField(upload_to='devwa/odyo/', blank=True, null=True, help_text="Si se yon odyo pou yo koute (.mp3)")
    lyen_videyo = models.URLField(blank=True, null=True, help_text="Lyen videyo (YouTube, Drive, etc.)")
    fichye_videyo = models.FileField(upload_to='devwa/videyo/', blank=True, null=True, help_text="Si se yon fichye videyo monte (.mp4)")
    
    date_limit = models.DateTimeField(help_text="Dat ak lè devwa sa a dwe remèt")

    class Meta:
        verbose_name_plural = "Devwa yo"

    def __str__(self):
        return self.tit
class Tes(models.Model):
    tit = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    duree_minit = models.IntegerField(default=30, help_text="Temps tès la ap dure (an minit)")
    lyen_tes = models.URLField(blank=True, null=True, help_text="Lyen tès la (Google Forms / Microsoft Forms / Platfòm)")

    class Meta:
        verbose_name_plural = "Tès ak Egzamen yo"

    def __str__(self):
        return self.tit     
class Setifika(models.Model):
    eleun = models.ForeignKey(User, on_delete=models.CASCADE)
    kou = models.ForeignKey(Kou, on_delete=models.CASCADE)
    fichye_pdf = models.FileField(upload_to='setifika_pdf/')
    date_emisyon = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Sètifika {self.eleun.username} - {self.kou.tit}"           


# Create your models here.
