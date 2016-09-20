# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('type', models.CharField(max_length=50, choices=[('bug', 'Signaler un bug'), ('amélioration', 'Suggérer une amélioration'), ('question', 'Poser une question'), ('commentaire', 'Faire un commentaire')])),
                ('description', models.TextField(verbose_name='Description', default=' ')),
                ('suggestion', models.TextField(verbose_name='Suggestion(s)', default=' ', null=True, blank=True)),
                ('nom', models.CharField(verbose_name='Votre nom', max_length=100)),
                ('email', models.EmailField(verbose_name='Votre adresse mail', max_length=254)),
                ('echelle', models.CharField(max_length=10, choices=[('1', '1 (Détail)'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5 (Important)'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10 (Essentiel)')])),
            ],
            options={
                'verbose_name': "Rapport sur l'utilisation de la carte",
                'managed': True,
            },
        ),
    ]
