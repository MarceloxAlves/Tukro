from django import forms
from .models import *
class PostagemForm(forms.ModelForm):
    class Meta:
        model =  Postagem
        fields =  [ 'texto','privacidade']
        widgets = {
            'texto' : forms.Textarea(attrs={'class':'form-control input-postagem', 'placeholder': 'O que você tem em mente hoje?', 'row':'2'}),
            'privacidade': forms.Select(attrs={'class':'form-control'}, choices=Postagem.PRIVACIDADES)
        }