# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dotalive', '0002_streams_anchorname'),
    ]

    operations = [
        migrations.CreateModel(
            name='stream_sites',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('site_name', models.CharField(max_length=20)),
                ('site_code', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='streams',
            name='website',
            field=models.ForeignKey(to='dotalive.stream_sites'),
            preserve_default=True,
        ),
    ]
