# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.gis.db.models.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('titre', models.CharField(verbose_name="Titre de l'action", max_length=100)),
                ('date_debut', models.DateField(verbose_name='Date de démarrage')),
                ('date_fin', models.DateField(verbose_name='Date de fin')),
                ('duree', models.CharField(blank=True, default='', verbose_name="Durée de l'action", max_length=40)),
                ('avancement', models.CharField(default='En cours', choices=[('En attente', 'En attente'), ('En cours', 'En cours'), ('Terminé', 'Terminé')], verbose_name="Etat d'avancement", max_length=10)),
                ('description', models.TextField(blank=True, default='', verbose_name="Description de l'action")),
                ('commentaire', models.TextField(blank=True, default='', verbose_name="Observations sur l'action")),
                ('montant_prevu', models.PositiveIntegerField(blank=True, verbose_name='Montant prévu', null=True)),
                ('montant_disponible', models.PositiveIntegerField(blank=True, verbose_name='Montant disponible', null=True)),
                ('devise', models.CharField(default='EUR', choices=[('MGA', 'MGA'), ('EUR', 'EUR'), ('USD', 'USD')], max_length=10)),
                ('bailleurfond', models.CharField(blank=True, default='', verbose_name='Bailleurs de fond', max_length=100)),
                ('origine', models.CharField(blank=True, default='', verbose_name='Origine de la donnée', max_length=100)),
                ('contact', models.EmailField(verbose_name="Mail du contact à l'origine de la donnée", max_length=100)),
                ('echelle_localisation', models.CharField(default='non', choices=[('non', 'Non'), ('oui', 'Oui')], verbose_name='Echelle nationale ?', max_length=10)),
                ('operateur', models.CharField(blank=True, default='', verbose_name="Opérateur en lien avec l'action", max_length=100)),
                ('resultat_cf_annee_ant', models.CharField(blank=True, default='', verbose_name="Résultat par rapport à l'année précédente", max_length=100)),
                ('priorite_psn', models.CharField(blank=True, default='', verbose_name="Priorité du PSN que l'activité appuie", max_length=100)),
                ('creation', models.DateTimeField(auto_now_add=True, verbose_name='Date de création fiche')),
                ('maj', models.DateTimeField(auto_now_add=True, verbose_name='Date de la dernière mise à jour fiche')),
                ('login_maj', models.DateTimeField(auto_now_add=True, verbose_name='Date de la dernière connection à la fiche action')),
            ],
            options={
                'verbose_name_plural': 'Actions',
                'verbose_name': 'Action',
                'ordering': ['-creation'],
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='ActionCible',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('action', models.ForeignKey(to='cnls.Action')),
            ],
            options={
                'verbose_name_plural': 'Cibles',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='ActionLocalisation',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('region_status', models.CharField(default='tananarive', choices=[('tananarive', 'Tananarive'), ('régionale', 'Régionale'), ('locale', 'Locale')], verbose_name="Définir la localisation de l'action ?", max_length=50)),
                ('choix_status', models.CharField(blank=True, default='', verbose_name='limite choisie', max_length=50)),
                ('geo', django.contrib.gis.db.models.fields.PointField(verbose_name='Cliquez sur la localisation', srid=4326)),
                ('action', models.ForeignKey(to='cnls.Action')),
            ],
            options={
                'verbose_name_plural': 'Localisation',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='ActionTypeintervention',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('objectif', models.PositiveIntegerField(blank=True, verbose_name='Nombre de personnes visées', null=True)),
            ],
            options={
                'verbose_name_plural': "Types d'intervention",
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Cible',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('nom', models.CharField(choices=[('population générale', 'Population générale'), ('adultes', 'Adultes'), ('personnes vivant avec le vih', 'Personnes vivant avec le VIH'), ('perdus de vue', 'Perdus de vue'), ('personnes vivant avec le vih', 'Personnes vivant avec le VIH'), ('perdus de vue', 'Perdus de vue'), ('consommateurs de drogues injectables', 'Consommateurs de drogues injectables'), ('homme ayant des rapports avec d’autres hommes', 'Homme ayant des rapports avec d’autres hommes'), ('travailleuses du sexe', 'Travailleuses du sexe'), ('hommes à comportements à hauts risques', 'Hommes à comportements à hauts risques'), ('clients des tds', 'Clients des TdS'), ('populations migrantes', 'Populations migrantes'), ('population carcérale', 'Population carcérale'), ('forces armées', 'Forces armées'), ('femmes enceintes', 'Femmes enceintes'), ('femmes victimes de violences sexuelles', 'Femmes victimes de violences sexuelles'), ('leaders religieux ou traditionnels', 'Leaders religieux ou traditionnels'), ('personnels de santé', 'Personnels de santé'), ('autres (cercles associatifs, cercles religieux, etc)', 'Autres (Cercles associatifs, cercles religieux, etc)'), ('jeunes', 'Jeunes'), ('jeunes scolarisés', 'Jeunes scolarisés'), ('jeunes non-scolarisés', 'Jeunes non-scolarisés'), ('orphelins et enfants vulnérables', 'Orphelins et Enfants Vulnérables')], max_length=40)),
            ],
            options={
                'verbose_name_plural': 'Cibles',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Organisme',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('nom', models.CharField(unique=True, max_length=40)),
                ('description', models.TextField(blank=True, default='')),
                ('logo', models.ImageField(blank=True, default='static/media/logo/defaultLogo.png', upload_to='static/media/logo/')),
                ('referent', models.ForeignKey(null=True, to='cnls.Organisme', blank=True)),
            ],
            options={
                'verbose_name_plural': 'Organismes',
                'verbose_name': 'Organisme',
                'ordering': ['nom'],
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('nom', models.CharField(unique=True, choices=[('Partenaire sur une Action', 'Partenaire'), ('Bailleur', 'Bailleur'), ("Organisme maître d'œuvre", 'Organisme')], max_length=40)),
            ],
            options={
                'verbose_name_plural': 'Status',
            },
        ),
        migrations.CreateModel(
            name='Typeintervention',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('nom', models.CharField(choices=[('plaidoyer', 'Plaidoyer'), ('ccc', 'CCC'), ('promotion de préservatifs', 'Promotion de préservatifs'), ('communication de masse', 'Communication de masse'), ('prise en charge IST', 'Prise en charge IST'), ('prise en charge médicale', 'Prise en charge médicale'), ('soutien', 'Soutien'), ('coordination', 'Coordination'), ('renforcement de capacités', 'Renforcement de capacités')], max_length=40)),
            ],
            options={
                'verbose_name_plural': "Types d'intervention",
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Utilisateur',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('photo', models.ImageField(blank=True, default='static/media/photos/defaultPicture.png', upload_to='static/media/photos/')),
                ('is_responsable', models.BooleanField(default=False, verbose_name='Responsable autorisé à éditer la fiche')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Utilisateurs',
                'verbose_name': 'Utilisateur',
                'ordering': ['user'],
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='actiontypeintervention',
            name='Typeintervention',
            field=models.ForeignKey(to='cnls.Typeintervention'),
        ),
        migrations.AddField(
            model_name='actiontypeintervention',
            name='action',
            field=models.ForeignKey(to='cnls.Action'),
        ),
        migrations.AddField(
            model_name='actioncible',
            name='cible',
            field=models.ForeignKey(to='cnls.Cible'),
        ),
        migrations.AddField(
            model_name='action',
            name='createur',
            field=models.ForeignKey(verbose_name='Nom du responsable de la fiche', to='cnls.Utilisateur'),
        ),
        migrations.AddField(
            model_name='action',
            name='organisme',
            field=models.ForeignKey(verbose_name="Organisme maître d'œuvre", to='cnls.Organisme'),
        ),
    ]
