from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

# 1. Modèl Profil Itilizatè (Jere WhatsApp ak aksè 24h gratis)
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    whatsapp_number = models.CharField(max_length=20, verbose_name="Nimewo WhatsApp")
    level = models.CharField(max_length=10, blank=True, null=True, verbose_name="Nivo")
    is_paid = models.BooleanField(default=False, verbose_name="Èske l peye?")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Dat Enskripsyon")

    def __str__(self):
        return f"{self.user.username} - {self.whatsapp_number}"

    @property
    def gen_akse(self):
        if self.is_paid:
            return True
        limit_24h = self.created_at + timedelta(hours=24)
        return timezone.now() <= limit_24h


# 2. Modèl Nivo Kou (Level A1 Debutant, A2, etc.)
class NivoKou(models.Model):
    nom = models.CharField(max_length=100, verbose_name="Non Nivo a")
    deskripsyon = models.TextField(blank=True, null=True, verbose_name="Deskripsyon Nivo a")

    def __str__(self):
        return self.nom

    class Meta:
        verbose_name = "Nivo Kou"
        verbose_name_plural = "Nivo Kou yo"
class Profil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profil')
    telephone = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.user.username} - {self.telephone}"


# 3. Modèl Leson Kou (Gen kontni tèks, dokiman, videyo ak odyo ansanm)
class LesonKou(models.Model):
    nivo = models.ForeignKey(NivoKou, on_delete=models.CASCADE, related_name='leson_yo', verbose_name="Nivo")
    titre = models.CharField(max_length=200, verbose_name="Tit Leson an")
    kontni = models.TextField(verbose_name="Eksplikasyon Leson an", blank=True, null=True)

    vimeo_url = models.CharField(max_length=500, blank=True, null=True, verbose_name="Lyen  Vimeo")
    zoom_url = models.URLField(max_length=500, blank=True, null=True, verbose_name="Lyen Anrejistreman Zoom")

    # Chan pou Fichye Medya ak Dokiman anndan leson an
    fichye_dokiman = models.FileField(upload_to='leson_dokiman/', blank=True, null=True, verbose_name="Dokiman (PDF/Word)")
    fichye_videyo = models.FileField(upload_to='leson_videyo/', blank=True, null=True, verbose_name="Videyo Leson an")
    fichye_odyo = models.FileField(upload_to='leson_odyo/', blank=True, null=True, verbose_name="Odyo Leson an")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nivo.nom} - {self.titre}"

    class Meta:
        verbose_name = "Leson Kou"
        verbose_name_plural = "Leson Kou yo"



class Devwa(models.Model):
    leson = models.ForeignKey('LesonKou', on_delete=models.CASCADE, related_name='devwa_yo', null=True, blank=True)
    titre = models.CharField(max_length=200)
    deskripsyon = models.TextField(blank=True, null=True)
    date_limite = models.DateTimeField()  # Dat ak lè limit devwa a

    fichye_konsiy = models.FileField(upload_to='devwa_konsiy/', blank=True, null=True, verbose_name="Fichye PDF Libellé Devwa")



    def est_expire(self):
        # Tcheke si dat limit la depase kounye a
        return timezone.now() > self.date_limite

    def __str__(self):
        return self.titre


class SoumisyonDevwa(models.Model):
    devwa = models.ForeignKey(Devwa, on_delete=models.CASCADE, related_name='soumisyon_yo')
    etidyan = models.ForeignKey(User, on_delete=models.CASCADE)
    fichye_or_repons = models.TextField("Repons/Lyen Devwa")
    date_soumisyon = models.DateTimeField(auto_now_add=True)
    fichye_repons = models.FileField(upload_to='devwa_repons/', blank=True, null=True, verbose_name="Fichye Devwa Etidyan")
    fichye_or_repons = models.TextField("Repons Tèks", blank=True, null=True)
    note = models.IntegerField("Nòt /100", null=True, blank=True)  # Nòt pwofesè a ap mete
    komanter_pwofese = models.TextField("Kòmantè Pwofesè", null=True, blank=True)

    def __str__(self):
        return f"{self.etidyan.username} - {self.devwa.titre}"


# 5. Modèl Tès / Exam
class Tes(models.Model):
    titre = models.CharField(max_length=200)

    def __str__(self):
        return self.titre
