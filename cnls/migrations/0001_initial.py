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
            name='ActionLocale',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('titre', models.CharField(max_length=250, verbose_name="Titre de l'action")),
                ('objectif', models.PositiveIntegerField(blank=True, null=True, verbose_name='Nombre de personnes visées')),
                ('date_debut', models.DateField(verbose_name='Date de démarrage')),
                ('date_fin', models.DateField(verbose_name='Date de fin')),
                ('duree', models.CharField(max_length=40, blank=True, verbose_name="Durée de l'action", default='')),
                ('avancement', models.CharField(max_length=10, choices=[('en attente', 'En attente'), ('en cours', 'En cours'), ('termine', 'Terminé')], verbose_name="État d'avancement", default='en cours')),
                ('description', models.TextField(blank=True, verbose_name="Description de l'action", default='')),
                ('commentaire', models.TextField(blank=True, verbose_name="Observations sur l'action", default='')),
                ('montant_prevu', models.PositiveIntegerField(blank=True, null=True, verbose_name='Montant prévu')),
                ('montant_disponible', models.PositiveIntegerField(blank=True, null=True, verbose_name='Montant disponible')),
                ('devise', models.CharField(max_length=10, choices=[('MGA', 'MGA'), ('EUR', 'EUR'), ('USD', 'USD')], default='EUR')),
                ('bailleurfond', models.CharField(max_length=100, blank=True, verbose_name='Bailleurs de fond', default='')),
                ('origine', models.CharField(max_length=100, blank=True, verbose_name='Origine de la donnée', default='')),
                ('contact', models.EmailField(max_length=100, verbose_name="Mail du contact à l'origine de la donnée")),
                ('operateur', models.CharField(max_length=100, blank=True, verbose_name="Opérateur en lien avec l'action", default='')),
                ('resultat_cf_annee_ant', models.CharField(max_length=250, blank=True, verbose_name="Résultat par rapport à l'année précédente", default='')),
                ('priorite_psn', models.CharField(max_length=100, blank=True, verbose_name="Priorité du PSN que l'activité appuie", default='')),
                ('latitude', models.DecimalField(null=True, verbose_name='Latitude', max_digits=10, default=-18.933333, decimal_places=6, blank=True)),
                ('longitude', models.DecimalField(null=True, verbose_name='Longitude', max_digits=10, default=47.516667, decimal_places=6, blank=True)),
                ('mpoint', django.contrib.gis.db.models.fields.PointField(srid=4326, default='SRID=4326;POINT(0.0 0.0)')),
                ('creation', models.DateTimeField(auto_now_add=True, verbose_name='Date de création fiche')),
                ('maj', models.DateTimeField(auto_now_add=True, verbose_name='Date de la dernière mise à jour fiche')),
                ('login_maj', models.DateTimeField(auto_now_add=True, verbose_name='Date de la dernière connection à la fiche action')),
                ('echelle_localisation', models.CharField(max_length=10, verbose_name="Échelle de l'action", default='locale')),
            ],
            options={
                'verbose_name': "'Action au niveau communal'",
                'verbose_name_plural': 'Actions au niveau communal',
            },
        ),
        migrations.CreateModel(
            name='ActionNationale',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('titre', models.CharField(max_length=250, verbose_name="Titre de l'action")),
                ('objectif', models.PositiveIntegerField(blank=True, null=True, verbose_name='Nombre de personnes visées')),
                ('date_debut', models.DateField(verbose_name='Date de démarrage')),
                ('date_fin', models.DateField(verbose_name='Date de fin')),
                ('duree', models.CharField(max_length=40, blank=True, verbose_name="Durée de l'action", default='')),
                ('avancement', models.CharField(max_length=10, choices=[('en attente', 'En attente'), ('en cours', 'En cours'), ('termine', 'Terminé')], verbose_name="État d'avancement", default='en cours')),
                ('description', models.TextField(blank=True, verbose_name="Description de l'action", default='')),
                ('commentaire', models.TextField(blank=True, verbose_name="Observations sur l'action", default='')),
                ('montant_prevu', models.PositiveIntegerField(blank=True, null=True, verbose_name='Montant prévu')),
                ('montant_disponible', models.PositiveIntegerField(blank=True, null=True, verbose_name='Montant disponible')),
                ('devise', models.CharField(max_length=10, choices=[('MGA', 'MGA'), ('EUR', 'EUR'), ('USD', 'USD')], default='EUR')),
                ('bailleurfond', models.CharField(max_length=100, blank=True, verbose_name='Bailleurs de fond', default='')),
                ('origine', models.CharField(max_length=100, blank=True, verbose_name='Origine de la donnée', default='')),
                ('contact', models.EmailField(max_length=100, verbose_name="Mail du contact à l'origine de la donnée")),
                ('operateur', models.CharField(max_length=100, blank=True, verbose_name="Opérateur en lien avec l'action", default='')),
                ('resultat_cf_annee_ant', models.CharField(max_length=250, blank=True, verbose_name="Résultat par rapport à l'année précédente", default='')),
                ('priorite_psn', models.CharField(max_length=100, blank=True, verbose_name="Priorité du PSN que l'activité appuie", default='')),
                ('latitude', models.DecimalField(null=True, verbose_name='Latitude', max_digits=10, default=-18.933333, decimal_places=6, blank=True)),
                ('longitude', models.DecimalField(null=True, verbose_name='Longitude', max_digits=10, default=47.516667, decimal_places=6, blank=True)),
                ('mpoint', django.contrib.gis.db.models.fields.PointField(srid=4326, default='SRID=4326;POINT(0.0 0.0)')),
                ('creation', models.DateTimeField(auto_now_add=True, verbose_name='Date de création fiche')),
                ('maj', models.DateTimeField(auto_now_add=True, verbose_name='Date de la dernière mise à jour fiche')),
                ('login_maj', models.DateTimeField(auto_now_add=True, verbose_name='Date de la dernière connection à la fiche action')),
                ('echelle_localisation', models.CharField(max_length=10, verbose_name="Échelle de l'action", default='nationale')),
            ],
            options={
                'verbose_name': "'Action au niveau national'",
                'verbose_name_plural': '   Actions au niveau national',
            },
        ),
        migrations.CreateModel(
            name='ActionRegionale',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('titre', models.CharField(max_length=250, verbose_name="Titre de l'action")),
                ('objectif', models.PositiveIntegerField(blank=True, null=True, verbose_name='Nombre de personnes visées')),
                ('date_debut', models.DateField(verbose_name='Date de démarrage')),
                ('date_fin', models.DateField(verbose_name='Date de fin')),
                ('duree', models.CharField(max_length=40, blank=True, verbose_name="Durée de l'action", default='')),
                ('avancement', models.CharField(max_length=10, choices=[('en attente', 'En attente'), ('en cours', 'En cours'), ('termine', 'Terminé')], verbose_name="État d'avancement", default='en cours')),
                ('description', models.TextField(blank=True, verbose_name="Description de l'action", default='')),
                ('commentaire', models.TextField(blank=True, verbose_name="Observations sur l'action", default='')),
                ('montant_prevu', models.PositiveIntegerField(blank=True, null=True, verbose_name='Montant prévu')),
                ('montant_disponible', models.PositiveIntegerField(blank=True, null=True, verbose_name='Montant disponible')),
                ('devise', models.CharField(max_length=10, choices=[('MGA', 'MGA'), ('EUR', 'EUR'), ('USD', 'USD')], default='EUR')),
                ('bailleurfond', models.CharField(max_length=100, blank=True, verbose_name='Bailleurs de fond', default='')),
                ('origine', models.CharField(max_length=100, blank=True, verbose_name='Origine de la donnée', default='')),
                ('contact', models.EmailField(max_length=100, verbose_name="Mail du contact à l'origine de la donnée")),
                ('operateur', models.CharField(max_length=100, blank=True, verbose_name="Opérateur en lien avec l'action", default='')),
                ('resultat_cf_annee_ant', models.CharField(max_length=250, blank=True, verbose_name="Résultat par rapport à l'année précédente", default='')),
                ('priorite_psn', models.CharField(max_length=100, blank=True, verbose_name="Priorité du PSN que l'activité appuie", default='')),
                ('latitude', models.DecimalField(null=True, verbose_name='Latitude', max_digits=10, default=-18.933333, decimal_places=6, blank=True)),
                ('longitude', models.DecimalField(null=True, verbose_name='Longitude', max_digits=10, default=47.516667, decimal_places=6, blank=True)),
                ('mpoint', django.contrib.gis.db.models.fields.PointField(srid=4326, default='SRID=4326;POINT(0.0 0.0)')),
                ('creation', models.DateTimeField(auto_now_add=True, verbose_name='Date de création fiche')),
                ('maj', models.DateTimeField(auto_now_add=True, verbose_name='Date de la dernière mise à jour fiche')),
                ('login_maj', models.DateTimeField(auto_now_add=True, verbose_name='Date de la dernière connection à la fiche action')),
                ('echelle_localisation', models.CharField(max_length=10, verbose_name="Échelle de l'action", default='régionale')),
            ],
            options={
                'verbose_name': "'Action au niveau régional'",
                'verbose_name_plural': ' Actions au niveau régional',
            },
        ),
        migrations.CreateModel(
            name='ActionTananarive',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('titre', models.CharField(max_length=250, verbose_name="Titre de l'action")),
                ('objectif', models.PositiveIntegerField(blank=True, null=True, verbose_name='Nombre de personnes visées')),
                ('date_debut', models.DateField(verbose_name='Date de démarrage')),
                ('date_fin', models.DateField(verbose_name='Date de fin')),
                ('duree', models.CharField(max_length=40, blank=True, verbose_name="Durée de l'action", default='')),
                ('avancement', models.CharField(max_length=10, choices=[('en attente', 'En attente'), ('en cours', 'En cours'), ('termine', 'Terminé')], verbose_name="État d'avancement", default='en cours')),
                ('description', models.TextField(blank=True, verbose_name="Description de l'action", default='')),
                ('commentaire', models.TextField(blank=True, verbose_name="Observations sur l'action", default='')),
                ('montant_prevu', models.PositiveIntegerField(blank=True, null=True, verbose_name='Montant prévu')),
                ('montant_disponible', models.PositiveIntegerField(blank=True, null=True, verbose_name='Montant disponible')),
                ('devise', models.CharField(max_length=10, choices=[('MGA', 'MGA'), ('EUR', 'EUR'), ('USD', 'USD')], default='EUR')),
                ('bailleurfond', models.CharField(max_length=100, blank=True, verbose_name='Bailleurs de fond', default='')),
                ('origine', models.CharField(max_length=100, blank=True, verbose_name='Origine de la donnée', default='')),
                ('contact', models.EmailField(max_length=100, verbose_name="Mail du contact à l'origine de la donnée")),
                ('operateur', models.CharField(max_length=100, blank=True, verbose_name="Opérateur en lien avec l'action", default='')),
                ('resultat_cf_annee_ant', models.CharField(max_length=250, blank=True, verbose_name="Résultat par rapport à l'année précédente", default='')),
                ('priorite_psn', models.CharField(max_length=100, blank=True, verbose_name="Priorité du PSN que l'activité appuie", default='')),
                ('latitude', models.DecimalField(null=True, verbose_name='Latitude', max_digits=10, default=-18.933333, decimal_places=6, blank=True)),
                ('longitude', models.DecimalField(null=True, verbose_name='Longitude', max_digits=10, default=47.516667, decimal_places=6, blank=True)),
                ('mpoint', django.contrib.gis.db.models.fields.PointField(srid=4326, default='SRID=4326;POINT(0.0 0.0)')),
                ('creation', models.DateTimeField(auto_now_add=True, verbose_name='Date de création fiche')),
                ('maj', models.DateTimeField(auto_now_add=True, verbose_name='Date de la dernière mise à jour fiche')),
                ('login_maj', models.DateTimeField(auto_now_add=True, verbose_name='Date de la dernière connection à la fiche action')),
                ('echelle_localisation', models.CharField(max_length=10, verbose_name="Échelle de l'action", default='Tananarive')),
            ],
            options={
                'verbose_name': "'Action dans la capitale'",
                'verbose_name_plural': '  Actions dans la capitale',
            },
        ),
        migrations.CreateModel(
            name='Cible',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('nom', models.CharField(max_length=80, choices=[('population générale', 'Population générale'), ('adultes', 'Adultes'), ('personnes vivant avec le vih', 'Personnes vivant avec le VIH'), ('perdus de vue', 'Perdus de vue'), ('consommateurs de drogues injectables', 'Consommateurs de drogues injectables'), ('homme ayant des rapports avec d’autres hommes', 'Homme ayant des rapports avec d’autres hommes'), ('travailleuses du sexe', 'Travailleuses du sexe'), ('hommes à comportements à hauts risques', 'Hommes à comportements à hauts risques'), ('clients des tds', 'Clients des TdS'), ('populations migrantes', 'Populations migrantes'), ('population carcérale', 'Population carcérale'), ('forces armées', 'Forces armées'), ('femmes enceintes', 'Femmes enceintes'), ('femmes victimes de violences sexuelles', 'Femmes victimes de violences sexuelles'), ('leaders religieux ou traditionnels', 'Leaders religieux ou traditionnels'), ('personnels de santé', 'Personnels de santé'), ('autres (cercles associatifs, cercles religieux, etc)', 'Autres (Cercles associatifs, cercles religieux, etc)'), ('jeunes', 'Jeunes'), ('jeunes scolarisés', 'Jeunes scolarisés'), ('jeunes non-scolarisés', 'Jeunes non-scolarisés'), ('orphelins et enfants vulnérables', 'Orphelins et Enfants Vulnérables')])),
            ],
            options={
                'verbose_name_plural': 'Cibles',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Commune',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('nom', models.CharField(max_length=50, verbose_name='Nom de la commune', default='')),
                ('mpoint', django.contrib.gis.db.models.fields.PointField(srid=4326, verbose_name='Coordonnées de la commmune', default='SRID=4326;POINT(0.0 0.0)')),
            ],
            options={
                'verbose_name': 'Commune',
                'verbose_name_plural': 'Communes',
            },
        ),
        migrations.CreateModel(
            name='Fokontany',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('nom', models.CharField(max_length=50, verbose_name='Nom du fokontany', default='')),
                ('mpoint', django.contrib.gis.db.models.fields.PointField(srid=4326, verbose_name='Coordonnées du fokontany', default='SRID=4326;POINT(0.0 0.0)')),
            ],
            options={
                'verbose_name': 'Fokontany',
                'verbose_name_plural': 'Fokontany(s)',
            },
        ),
        migrations.CreateModel(
            name='Organisme',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('nom', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True, default='')),
                ('logo', models.ImageField(blank=True, upload_to='static/media/logo/', default='static/media/logo/defaultLogo.png')),
                ('referent', models.ForeignKey(null=True, to='cnls.Organisme', blank=True)),
            ],
            options={
                'verbose_name': 'Organisme',
                'verbose_name_plural': 'Organismes',
                'managed': True,
                'ordering': ['nom'],
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('nom', models.CharField(max_length=50, verbose_name='Nom de la région', default='')),
                ('mpoint', django.contrib.gis.db.models.fields.PointField(srid=4326, verbose_name='Coordonnées de la capitale de région', default='SRID=4326;POINT(0.0 0.0)')),
            ],
            options={
                'verbose_name': 'Région',
                'verbose_name_plural': 'Régions',
            },
        ),
        migrations.CreateModel(
            name='Typeintervention',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('nom', models.CharField(max_length=40, choices=[('plaidoyer', 'Plaidoyer'), ('ccc', 'CCC'), ('promotion de préservatifs', 'Promotion de préservatifs'), ('communication de masse', 'Communication de masse'), ('prise en charge IST', 'Prise en charge IST'), ('prise en charge médicale', 'Prise en charge médicale'), ('soutien', 'Soutien'), ('coordination', 'Coordination'), ('renforcement de capacités', 'Renforcement de capacités')])),
                ('descriptif', models.TextField(blank=True, verbose_name="Description du type d'intervention", default='')),
            ],
            options={
                'verbose_name_plural': "Types d'intervention",
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Utilisateur',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('photo', models.ImageField(blank=True, upload_to='static/media/photos/', default='static/media/photos/defaultPicture.png')),
                ('is_responsable', models.BooleanField(verbose_name='Responsable autorisé à éditer la fiche', default=False)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Utilisateur',
                'verbose_name_plural': 'Utilisateurs',
                'managed': True,
                'ordering': ['user'],
            },
        ),
        migrations.AddField(
            model_name='actiontananarive',
            name='cible',
            field=models.ManyToManyField(to='cnls.Cible', verbose_name='Publics cibles'),
        ),
        migrations.AddField(
            model_name='actiontananarive',
            name='createur',
            field=models.ForeignKey(to='cnls.Utilisateur', verbose_name='Nom du responsable de la fiche'),
        ),
        migrations.AddField(
            model_name='actiontananarive',
            name='fokontany',
            field=models.ManyToManyField(to='cnls.Fokontany', verbose_name='Fokontany(s)'),
        ),
        migrations.AddField(
            model_name='actiontananarive',
            name='organisme',
            field=models.ForeignKey(to='cnls.Organisme', verbose_name="Organisme maître d'œuvre"),
        ),
        migrations.AddField(
            model_name='actiontananarive',
            name='typeintervention',
            field=models.ManyToManyField(to='cnls.Typeintervention', verbose_name="Types d'interventions"),
        ),
        migrations.AddField(
            model_name='actionregionale',
            name='cible',
            field=models.ManyToManyField(to='cnls.Cible', verbose_name='Publics cibles'),
        ),
        migrations.AddField(
            model_name='actionregionale',
            name='createur',
            field=models.ForeignKey(to='cnls.Utilisateur', verbose_name='Nom du responsable de la fiche'),
        ),
        migrations.AddField(
            model_name='actionregionale',
            name='organisme',
            field=models.ForeignKey(to='cnls.Organisme', verbose_name="Organisme maître d'œuvre"),
        ),
        migrations.AddField(
            model_name='actionregionale',
            name='region',
            field=models.ManyToManyField(to='cnls.Region', verbose_name='Régions'),
        ),
        migrations.AddField(
            model_name='actionregionale',
            name='typeintervention',
            field=models.ManyToManyField(to='cnls.Typeintervention', verbose_name="Types d'interventions"),
        ),
        migrations.AddField(
            model_name='actionnationale',
            name='cible',
            field=models.ManyToManyField(to='cnls.Cible', verbose_name='Publics cibles'),
        ),
        migrations.AddField(
            model_name='actionnationale',
            name='createur',
            field=models.ForeignKey(to='cnls.Utilisateur', verbose_name='Nom du responsable de la fiche'),
        ),
        migrations.AddField(
            model_name='actionnationale',
            name='organisme',
            field=models.ForeignKey(to='cnls.Organisme', verbose_name="Organisme maître d'œuvre"),
        ),
        migrations.AddField(
            model_name='actionnationale',
            name='typeintervention',
            field=models.ManyToManyField(to='cnls.Typeintervention', verbose_name="Types d'interventions"),
        ),
        migrations.AddField(
            model_name='actionlocale',
            name='cible',
            field=models.ManyToManyField(to='cnls.Cible', verbose_name='Publics cibles'),
        ),
        migrations.AddField(
            model_name='actionlocale',
            name='commune',
            field=models.ManyToManyField(to='cnls.Commune', verbose_name='Communes'),
        ),
        migrations.AddField(
            model_name='actionlocale',
            name='createur',
            field=models.ForeignKey(to='cnls.Utilisateur', verbose_name='Nom du responsable de la fiche'),
        ),
        migrations.AddField(
            model_name='actionlocale',
            name='organisme',
            field=models.ForeignKey(to='cnls.Organisme', verbose_name="Organisme maître d'œuvre"),
        ),
        migrations.AddField(
            model_name='actionlocale',
            name='typeintervention',
            field=models.ManyToManyField(to='cnls.Typeintervention', verbose_name="Types d'interventions"),
        ),
    ]
