from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render,  get_object_or_404
from django.utils import timezone


from .form import EnskripsyonForm
from .models import Devwa, Dokiman, EnstriksyonPeman, NivoKou, AkseEtidyan, PrevPeman, Setifika, Tes, VerifikasyonEmail
from .models import LesonKou


def enskripsyon(request):
    if request.method == 'POST':
        form = EnskripsyonForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # 1. Kreye aksè etidyan (poko aktif - gen_akse = False)
            AkseEtidyan.objects.create(etidyan=user, gen_akse=False)
            
            # 2. Jènere kòd verifikasyon 6 chif la
            verif, created = VerifikasyonEmail.objects.get_or_create(user=user)
            verif.jènere_kod()
            
            # 3. Voye imèl verifikasyon an bay etidyan an
            suje = "Kòd Verifikasyon - Elite English Academy"
            mesaj = (
                f"Bonjou {user.first_name},\n\n"
                f"Kòd verifikasyon imèl ou an se: {verif.kod}\n\n"
                f"Tanpri rantre kòd sa a sou sit la pou konfime imèl ou an.\n"
                f"Remak: Aksè ou nan kou yo ap aktivman lè w voye prèv peman an e ke admin lan valide l."
            )
            
            try:
                send_mail(suje, mesaj, settings.DEFAULT_FROM_EMAIL, [user.email])
            except Exception as e:
                messages.warning(request, "Nou pa t ka voye imèl la anrejistreman an fèt, tcheke konfigirasyon SMTP ou.")

            # Sere ID itilizatè a nan session la pou paj verifikasyon an
            request.session['user_id_pending'] = user.id
            return redirect('verifye_kod')
    else:
        form = EnskripsyonForm()
    return render(request, 'courses/enskripsyon.html', {'form': form})


def verifye_kod(request):
    user_id = request.session.get('user_id_pending')
    if not user_id:
        return redirect('enskripsyon')

    if request.method == 'POST':
        kod_antre = request.POST.get('kod')
        try:
            verif = VerifikasyonEmail.objects.get(user_id=user_id, kod=kod_antre)
            verif.estati_verifye = True
            verif.save()
            
            messages.success(request, "Imèl ou verifye ak siksè! Ou ka konekte kounye a.")
            del request.session['user_id_pending']
            return redirect('koneksyon')
        except VerifikasyonEmail.DoesNotExist:
            messages.error(request, "Kòd la pa bon! Tcheke imèl ou an ankò.")

    return render(request, 'courses/verifye_kod.html')


def koneksyon(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            
            # Tcheke si etidyan an gen aksè
            try:
                akse = AkseEtidyan.objects.get(etidyan=user)
                if akse.gen_akse:
                    return redirect('lis_kou')
                else:
                    return render(request, 'courses/block.html')
            except AkseEtidyan.DoesNotExist:
                return render(request, 'courses/block.html')
        else:
            messages.error(request, "Imèl oswa modpas la pa bon.")
            
    return render(request, 'courses/koneksyon.html')


def dekonksyon(request):
    logout(request)
    return redirect('koneksyon')


@login_required
def lis_kou(request):
    try:
        akse = AkseEtidyan.objects.get(etidyan=request.user)
        if not akse.gen_akse:
            return render(request, 'courses/block.html')
    except AkseEtidyan.DoesNotExist:
        return render(request, 'courses/block.html')

    nivo_yo = NivoKou.objects.all()
    return render(request, 'courses/lis_kou.html', {'nivo_yo': nivo_yo})


@login_required
def peman(request):
    if request.method == 'POST':
        metod = request.POST.get('metod_peman')
        tranzaksyon = request.POST.get('nimewo_tranzaksyon')
        resi = request.FILES.get('foto_resi')
        peman_info = EnstriksyonPeman.objects.first()

        PrevPeman.objects.create(
            user=request.user,
            metod_peman=metod,
            nimewo_tranzaksyon=tranzaksyon,
            foto_resi=resi
        )
        messages.success(request, "Prèv peman ou an voye ak siksè! Admin lan ap tcheke l pou l ba w aksè kòmsadwa.")
        return redirect('peman')
    
    # 1. Bay varyab la yon valè pa defo (None) anvan
    peman_info = None 
    
    # 2. Chèche premye enfòmasyon peman an si l egziste
    peman_info = EnstriksyonPeman.objects.first()

    # 3. Voye l bay template la
    

    return render(request, 'courses/peman.html',{
        'peman_info': peman_info
    })


@login_required
def detay_kou(request, leson_id):
    leson = get_object_or_404(LesonKou, id=leson_id)
    dokiman_lis = Dokiman.objects.all()
    devwa_lis = Devwa.objects.all()
    tes_lis = Tes.objects.all()
    setifika = None
    if request.user.is_authenticated:
        # LesonKou should have a relation to its parent course (kou)
        kou = getattr(leson, 'kou', None)
        setifika = Setifika.objects.filter(eleun=request.user, kou=kou).first()

    context = {
        'leson': leson,
        'kou': kou,
        'setifika': setifika,
        'dokiman_lis': dokiman_lis,
        'devwa_lis': devwa_lis,
        'tes_lis': tes_lis,
        'now': timezone.now(), # 👈 Django ap sèvi ak sa pou konpare ak lè devwa a!
    }

    return render(request, 'courses/detay_kou.html', context)