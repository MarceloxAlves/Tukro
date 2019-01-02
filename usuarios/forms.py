from django import forms
from django.contrib.auth.models import User
from perfis.views import get_perfil_logado

class RegistrarUsuarioForm(forms.Form):
    nome = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    senha = forms.CharField(required=True)
    telefone = forms.CharField(required=True)
    nome_empresa = forms.CharField(required=True)

    def is_valid(self):
        valid = True
        if not super(RegistrarUsuarioForm, self).is_valid():
            self.adiciona_erro('Por favor, verifique os dados informados')
            valid = False
        user_exists = User.objects.filter(username=self.cleaned_data['email']).exists()
        if user_exists:
            self.adiciona_erro('Usuário já existente.')
            valid = False
        return valid

    def adiciona_erro(self, message):
        errors = self._errors.setdefault(forms.forms.NON_FIELD_ERRORS,
                            forms.utils.ErrorList())
        errors.append(message)


class AlterarSenhaForm(forms.Form):
    password_atual = forms.CharField(required=True)
    new_password = forms.CharField(required=True)
    confirm_password = forms.CharField(required=True)

    def is_valid(self):
        valid = True
        usuario = get_perfil_logado()

        if not super(AlterarSenhaForm, self).is_valid():
            self.adiciona_erro('Por favor, verifique os dados')
            valid = False

        if not usuario.check_password(self.password_atual):
            self.adiciona_erro('Senha informada incorreta!')
            valid = False

        if self.new_password != self.confirm_password:
            self.adiciona_erro('Senhas informadas não conferem!')
            valid = False

        return valid

    def adiciona_erro(self, message):
        errors = self._errors.setdefault(forms.forms.NON_FIELD_ERRORS,
                                         forms.utils.ErrorList())
        errors.append(message)