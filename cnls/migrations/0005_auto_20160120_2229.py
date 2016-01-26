# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cnls', '0004_auto_20160120_2141'),
    ]

    operations = [
        migrations.RenameField(
            model_name='actionlocalisation',
            old_name='geom',
            new_name='geo',
        ),
    ]
