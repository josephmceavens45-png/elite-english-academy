from django import forms
from django.contrib.auth.models import User

class EnskripsyonForm(forms.ModelForm):
    first_name = forms.CharField(label="Prenon", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Prenon w'}))
    last_name = forms.CharField(label="Non", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Non w'}))
    email = forms.EmailField(label="Imel", widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'egzanp@gmail.com'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Imel sa a gen yon kont sou li deja. Tanpri kontakte administratè a.")
        return email