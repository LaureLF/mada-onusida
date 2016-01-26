# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cnls', '0006_auto_20160120_2237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='action',
            name='avancement',
            field=models.CharField(verbose_name="Etat d'avancement", default='en cours', max_length=10, choices=[('en attente', 'En attente'), ('en cours', 'En cours'), ('terminé', 'Terminé')]),
        ),
        migrations.AlterField(
            model_name='actionlocalisation',
            name='geo',
            field=django.contrib.gis.db.models.fields.PointField(verbose_name='Cliquez sur la localisation', default='SRID=4326;POINT(0.0 0.0)', srid=4326),
        ),
        migrations.AlterField(
            model_name='cible',
            name='nom',
            field=models.CharField(max_length=40, choices=[('population générale', 'Population générale'), ('adultes', 'Adultes'), ('personnes vivant avec le vih', 'Personnes vivant avec le VIH'), ('perdus de vue', 'Perdus de vue'), ('consommateurs de drogues injectables', 'Consommateurs de drogues injectables'), ('homme ayant des rapports avec d’autres hommes', 'Homme ayant des rapports avec d’autres hommes'), ('travailleuses du sexe', 'Travailleuses du sexe'), ('hommes à comportements à hauts risques', 'Hommes à comportements à hauts risques'), ('clients des tds', 'Clients des TdS'), ('populations migrantes', 'Populations migrantes'), ('population carcérale', 'Population carcérale'), ('forces armées', 'Forces armées'), ('femmes enceintes', 'Femmes enceintes'), ('femmes victimes de violences sexuelles', 'Femmes victimes de violences sexuelles'), ('leaders religieux ou traditionnels', 'Leaders religieux ou traditionnels'), ('personnels de santé', 'Personnels de santé'), ('autres (cercles associatifs, cercles religieux, etc)', 'Autres (Cercles associatifs, cercles religieux, etc)'), ('jeunes', 'Jeunes'), ('jeunes scolarisés', 'Jeunes scolarisés'), ('jeunes non-scolarisés', 'Jeunes non-scolarisés'), ('orphelins et enfants vulnérables', 'Orphelins et Enfants Vulnérables')]),
        ),
        migrations.AlterField(
            model_name='status',
            name='nom',
            field=models.CharField(unique=True, max_length=40, choices=[('partenaire', 'Partenaire sur une Action'), ('bailleur', 'Bailleur'), ('organisme', "Organisme maître d'œuvre")]),
        ),
    ]
