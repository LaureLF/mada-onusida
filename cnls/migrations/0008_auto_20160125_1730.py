# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cnls', '0007_auto_20160121_0115'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='action',
            unique_together=set([('titre', 'organisme', 'createur', 'creation')]),
        ),
    ]
