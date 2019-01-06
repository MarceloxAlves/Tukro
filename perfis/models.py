from django.db import models
from django.contrib.auth.models import User


class Perfil(models.Model):
    nome = models.CharField(max_length=255, null=False)
    telefone = models.CharField(max_length=15, null=False)
    nome_empresa = models.CharField(max_length=255, null=False)
    contatos = models.ManyToManyField('self')
    usuario = models.OneToOneField(User, related_name="perfil",
                                   on_delete=models.CASCADE)

    @property
    def email(self):
        return self.usuario.email

    def __str__(self):
        return self.nome

    def convidar(self, perfil_convidado):
        if self.pode_convidar(perfil_convidado):
            convite = Convite(solicitante=self, convidado=perfil_convidado)
            convite.save()

    def pode_convidar(self, perfil_convidado):
        return self.regras_convite(perfil_convidado)['pode']

    def regras_convite(self, perfil_convidado):
        recebidos = Convite.objects.filter(solicitante=perfil_convidado, convidado=self)
        enviados = Convite.objects.filter(solicitante=self, convidado=perfil_convidado)

        if perfil_convidado in self.contatos.all():
            return {'pode':False, 'motivo': 'friends'}
        elif enviados:
            return {'pode': False, 'motivo': 'send'}
        elif recebidos:
            return {'pode': False, 'motivo': 'received'}

        return {'pode': True}

    def desfazer_amizade(self, perfil_amigo):
        self.contatos.remove(perfil_amigo)
        perfil_amigo.contatos.remove(self)
        self.save()
        perfil_amigo.save()

    def get_postagens(self):
        postagens = []
        for post in self.timeline.all():
            postagens.append(post)
        for contato in self.contatos.all():
            for post in contato.timeline.all().exclude(privacidade='PRIVATE'):
                postagens.append(post)

        return sorted(postagens, key=Postagem.get_id, reverse=True)

    def get_public_perfil(self):
        postagens = []
        for post in self.timeline.filter(privacidade='PUBLIC'):
            postagens.append(post)
        return sorted(postagens, key=Postagem.get_id, reverse=True)


class Convite(models.Model):
    solicitante = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name='convites_feitos')
    convidado = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name='convites_recebidos')

    def aceitar(self):
        self.solicitante.contatos.add(self.convidado)
        self.convidado.contatos.add(self.solicitante)
        self.delete()

    def recusar(self):
        self.delete()


class Postagem(models.Model):
    PRIVACIDADES = (
        ('PUBLIC', 'Público'),
        ('FRIENDS','Amigos'),
        ('PRIVATE', 'Somente eu'),
    )

    texto = models.TextField()
    data = models.DateTimeField(auto_now=True)
    perfil = models.ForeignKey(Perfil, related_name='timeline', on_delete=models.CASCADE)
    privacidade = models.CharField(max_length=10, default='PUBLIC', choices=PRIVACIDADES)
    reactions = models.ManyToManyField(Perfil, through='Reaction')
    imagem = models.ImageField(upload_to='postagem', null=True)

    class Meta:
        ordering = ['-data']

    def get_id(self):
        return self.id

    def __str__(self):
        return self.texto


    def get_reaction_type(self):
        return  ReactionType.objects.all()

    def get_reacoes(self):
        return  Reaction.objects.filter(postagem=self)




class ReactionType(models.Model):
    label =  models.CharField(max_length=10)
    icon =  models.CharField(max_length=20)
    animation =  models.CharField(max_length=20, default='')
    color =  models.CharField(max_length=20, default='#CCC')


class Reaction(models.Model):
    perfil =  models.ForeignKey(Perfil, on_delete=models.CASCADE)
    postagem =  models.ForeignKey(Postagem, on_delete=models.CASCADE)
    tipo = models.ForeignKey(ReactionType, on_delete=models.CASCADE)


class Partilhamento(Postagem):
     post =  models.ForeignKey(Postagem, on_delete=models.CASCADE, related_name='partilhamentos')