from django.db import models, transaction
from django.contrib.auth.models import User
from itertools import chain

from perfis import utils


class Perfil(models.Model):
    nome = models.CharField(max_length=255, null=False)
    telefone = models.CharField(max_length=15, null=False)
    nome_empresa = models.CharField(max_length=255, null=False)
    imagem =  models.ImageField(upload_to='perfil', default='perfil/user.png')
    contatos = models.ManyToManyField('self')
    usuario = models.OneToOneField(User, related_name="perfil",
                                   on_delete=models.CASCADE)
    bloqueados = models.ManyToManyField('self')

    @property
    def email(self):
        return self.usuario.email

    def __str__(self):
        return self.nome

    @transaction.atomic
    def convidar(self, perfil_convidado):
        if self.pode_convidar(perfil_convidado):
            convite = Convite(solicitante=self, convidado=perfil_convidado)
            convite.save()

    @transaction.atomic
    def bloquear(self, perfil_bloqueado):
        self.bloqueados.add(perfil_bloqueado)
        self.desfazer_amizade(perfil_bloqueado)
        self.save()

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

    @transaction.atomic
    def desfazer_amizade(self, perfil_amigo):
        self.contatos.remove(perfil_amigo)
        perfil_amigo.contatos.remove(self)
        self.save()
        perfil_amigo.save()

    def get_postagens(self):
        postagens = []

        if self.usuario.is_superuser == True:
            postagens = list(chain(Postagem.objects.filter(tipo='POST'), Partilhamento.objects.filter(tipo='SHARE')))
        else:
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

    def get_justificativa(self):
        justificativas = self.usuario.justificativas.all()
        print(justificativas)
        if justificativas is not None:
            return justificativas[0]
        return None


class Convite(models.Model):
    solicitante = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name='convites_feitos')
    convidado = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name='convites_recebidos')

    @transaction.atomic
    def aceitar(self):
        self.solicitante.contatos.add(self.convidado)
        self.convidado.contatos.add(self.solicitante)
        self.delete()

    def recusar(self):
        self.delete()


class Hashtag(models.Model):
    label = models.CharField(max_length=255)


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
    hashtags = models.ManyToManyField(Hashtag, related_name='hashtags')
    imagem = models.ImageField(upload_to='postagem', null=True)
    tipo = models.CharField(max_length=10, default='POST')

    @property
    def post_partilhamento(self):
        if self.tipo == 'SHARE':
            partilha = Partilhamento.objects.get(id=self.id)
            return partilha.post
        return None

    @property
    def total_reactions(self):
        return  len(self.reaction_set.all())

    class Meta:
        ordering = ['-data']

    def get_id(self):
        return self.id

    def __str__(self):
        return self.texto

    def qtd_hashtags(self):
        return len(self.hashtags.all())

    def save(self):
        super(Postagem, self).save()
        hashs = utils.busca_palavra("#", self.texto)
        for hash in hashs:
            hashtag = Hashtag.objects.create(label=hash)
            self.hashtags.add(hashtag)
        super(Postagem, self).save()

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


class Justificativa(models.Model):
    texto = models.CharField(max_length=200);
    user  =  models.ForeignKey(User, on_delete=models.CASCADE, related_name= 'justificativas')
    data_bloqueio = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['-data_bloqueio']
