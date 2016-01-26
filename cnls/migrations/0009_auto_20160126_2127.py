# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cnls', '0008_auto_20160125_1730'),
    ]

    operations = [
        migrations.AlterField(
            model_name='action',
            name='avancement',
            field=models.CharField(choices=[('en attente', 'En attente'), ('en cours', 'En cours'), ('termine', 'Terminé')], default='en cours', max_length=10, verbose_name="Etat d'avancement"),
        ),
        migrations.AlterField(
            model_name='action',
            name='resultat_cf_annee_ant',
            field=models.CharField(default='', max_length=250, blank=True, verbose_name="Résultat par rapport à l'année précédente"),
        ),
        migrations.AlterField(
            model_name='action',
            name='titre',
            field=models.CharField(max_length=250, verbose_name="Titre de l'action"),
        ),
        migrations.AlterField(
            model_name='cible',
            name='nom',
            field=models.CharField(choices=[('population générale', 'Population générale'), ('adultes', 'Adultes'), ('personnes vivant avec le vih', 'Personnes vivant avec le VIH'), ('perdus de vue', 'Perdus de vue'), ('consommateurs de drogues injectables', 'Consommateurs de drogues injectables'), ('homme ayant des rapports avec d’autres hommes', 'Homme ayant des rapports avec d’autres hommes'), ('travailleuses du sexe', 'Travailleuses du sexe'), ('hommes à comportements à hauts risques', 'Hommes à comportements à hauts risques'), ('clients des tds', 'Clients des TdS'), ('populations migrantes', 'Populations migrantes'), ('population carcérale', 'Population carcérale'), ('forces armées', 'Forces armées'), ('femmes enceintes', 'Femmes enceintes'), ('femmes victimes de violences sexuelles', 'Femmes victimes de violences sexuelles'), ('leaders religieux ou traditionnels', 'Leaders religieux ou traditionnels'), ('personnels de santé', 'Personnels de santé'), ('autres (cercles associatifs, cercles religieux, etc)', 'Autres (Cercles associatifs, cercles religieux, etc)'), ('jeunes', 'Jeunes'), ('jeunes scolarisés', 'Jeunes scolarisés'), ('jeunes non-scolarisés', 'Jeunes non-scolarisés'), ('orphelins et enfants vulnérables', 'Orphelins et Enfants Vulnérables')], max_length=80),
        ),
        migrations.AlterField(
            model_name='organisme',
            name='nom',
            field=models.CharField(unique=True, max_length=100),
        ),
    ]
