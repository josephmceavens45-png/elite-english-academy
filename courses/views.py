from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import UserProfile, NivoKou, LesonKou, Devwa, Tes, SoumisyonDevwa


# 1. Paj Enskripsyon (Aksè 24h Gratis + WhatsApp Int'l)
def enskripsyon(request):
    if request.user.is_authenticated:
        return redirect('lis_kou')

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        whatsapp_number = request.POST.get('whatsapp_number')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Tcheke si modpas yo matche
        if password != confirm_password:
            messages.error(request, "Modpas yo pa menm! Tanpri tcheke yo byen.")
            return render(request, 'courses/enskripsyon.html')

        # Tcheke si username la deja egziste
        if User.objects.filter(username=username).exists():
            messages.error(request, "Non itilizatè (username) sa a deja pran. Chwazi yon lòt.")
            return render(request, 'courses/enskripsyon.html')

        # Kreye itilizatè a
        user = User.objects.create_user(username=username, email=email, password=password)

        # Kreye profil itilizatè a ak nimewo WhatsApp li
        UserProfile.objects.create(
            user=user,
            whatsapp_number=whatsapp_number
        )

        # Voye Imèl Byenvini (Gmail) si etidyan an te rantre yon imèl
        if email:
            try:
                send_mail(
                    'Byenvini nan Elite English Academy!',
                    f'Bonjou {username},\n\nKont ou an kreye ak siksè! Ou gen 24h aksè gratis nan tout kou yo.',
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=True,
                )
            except Exception as e:
                messages.error(request, f"Kont lan kreye, men imèl la pa voye paske: {e}")

        # Konekte itilizatè a dirèkteman epi voye l sou paj kou yo
        login(request, user)
        messages.success(request, "Aktivasyon reyisi! Ou jwenn 24h aksè gratis nan tout kou yo.")
        return redirect('lis_kou')

    return render(request, 'courses/enskripsyon.html')


# 2. Paj Koneksyon (Login)
def koneksyon(request):
    if request.user.is_authenticated:
        return redirect('lis_kou')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('lis_kou')
        else:
            messages.error(request, "Non itilizatè oswa modpas la pa kòrèk.")

    return render(request, 'courses/login.html')


# 3. Dekoneksyon (Logout)
def dekoneksyon(request):
    logout(request)
    return redirect('koneksyon')


# 4. Paj Klas ak Kou yo
@login_required
def lis_kou(request):
    nivo_yo = NivoKou.objects.all()

    context = {
        'nivo_yo': nivo_yo,
    }
    return render(request, 'courses/lis_kou.html', context)


# 5. Jere Soumisyon Devwa (Gère Text + Fichye Upload yo)
@login_required
def soumet_devwa(request, devwa_id):
    devwa = get_object_or_404(Devwa, id=devwa_id)
    soumisyon = SoumisyonDevwa.objects.filter(devwa=devwa, etidyan=request.user).first()

    if request.method == 'POST':
        repons = request.POST.get('repons', '')
        fichye = request.FILES.get('fichye_repons')  # Pou pran fichye etidyan an upload sou aparèy li

        if soumisyon:
            if repons:
                soumisyon.fichye_or_repons = repons
            if fichye:
                soumisyon.fichye_repons = fichye
            soumisyon.save()
            messages.success(request, "Devwa w la mete ajour ak siksè!")
        else:
            SoumisyonDevwa.objects.create(
                devwa=devwa,
                etidyan=request.user,
                fichye_or_repons=repons,
                fichye_repons=fichye
            )
            messages.success(request, "Devwa w la voye ak siksè!")

        return redirect('lis_kou')

    return redirect('lis_kou')
