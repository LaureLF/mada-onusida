# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cnls', '0002_auto_20160120_1700'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actionlocalisation',
            name='geo',
            field=django.contrib.gis.db.models.fields.PointField(srid=4326, default='SRID=3857;POINT(0.0 0.0)', verbose_name='Cliquez sur la localisation'),
        ),
    ]
