# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cnls', '0005_auto_20160120_2229'),
    ]

    operations = [
        migrations.RenameField(
            model_name='actiontypeintervention',
            old_name='Typeintervention',
            new_name='typeintervention',
        ),
    ]
