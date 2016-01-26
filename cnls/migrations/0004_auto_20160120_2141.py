# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cnls', '0003_auto_20160120_1712'),
    ]

    operations = [
        migrations.RenameField(
            model_name='actionlocalisation',
            old_name='geo',
            new_name='geom',
        ),
    ]
