from django.db import models
from django.contrib.auth.models import User

class Perfil(models.Model):
    nome = models.CharField(max_length=255, null=False)
    telefone = models.CharField(max_length=15, null=False)
    nome_empresa =  models.CharField(max_length=255, null=False)
    contatos = models.ManyToManyField('self')
    usuario = models.OneToOneField(User, related_name="perfil",
    on_delete = models.CASCADE)

    @property
    def email(self):
        return self.usuario.email

    def __str__(self):
        return self.nome

    def convidar(self, perfil_convidado):
        if self.pode_convidar(perfil_convidado):
            convite = Convite(solicitante=self,convidado = perfil_convidado)
            convite.save()

    def pode_convidar(self, perfil_convidado):
        return True if not perfil_convidado in self.contatos.all() else False


class Convite(models.Model):
    solicitante = models.ForeignKey(Perfil,on_delete=models.CASCADE,related_name='convites_feitos' )
    convidado = models.ForeignKey(Perfil, on_delete= models.CASCADE, related_name='convites_recebidos')

    def aceitar(self):
        self.solicitante.contatos.add(self.convidado)
        self.convidado.contatos.add(self.solicitante)
        self.delete()

class Postagem(models.Model):
    texto = models.TextField()
    data = models.DateTimeField(auto_now=True)
    perfil = models.ForeignKey(Perfil, related_name='timeline', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-data']

    def __str__(self):
        return self.texto
