# Generated by Django 2.1.3 on 2019-01-07 23:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perfis', '0005_auto_20190106_2223'),
    ]

    operations = [
        migrations.AddField(
            model_name='perfil',
            name='bloqueados',
            field=models.ManyToManyField(related_name='_perfil_bloqueados_+', to='perfis.Perfil'),
        ),
    ]
