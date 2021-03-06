# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0013_userinfo_applyteamtime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='department',
            field=models.CharField(default=b'', max_length=10, choices=[(b'', b''), ((b'\xe6\x9c\xba\xe6\xa2\xb0\xe7\xb3\xbb',), b'\xe6\x9c\xba\xe6\xa2\xb0\xe7\xb3\xbb'), ((b'\xe7\x83\xad\xe8\x83\xbd\xe7\xb3\xbb',), b'\xe7\x83\xad\xe8\x83\xbd\xe7\xb3\xbb'), ((b'\xe7\x94\xb5\xe6\x9c\xba\xe7\xb3\xbb',), b'\xe7\x94\xb5\xe6\x9c\xba\xe7\xb3\xbb'), ((b'\xe7\x94\xb5\xe5\xad\x90\xe7\xb3\xbb',), b'\xe7\x94\xb5\xe5\xad\x90\xe7\xb3\xbb'), ((b'\xe8\xae\xa1\xe7\xae\x97\xe6\x9c\xba\xe7\xb3\xbb',), b'\xe8\xae\xa1\xe7\xae\x97\xe6\x9c\xba\xe7\xb3\xbb'), ((b'\xe8\x87\xaa\xe5\x8a\xa8\xe5\x8c\x96\xe7\xb3\xbb',), b'\xe8\x87\xaa\xe5\x8a\xa8\xe5\x8c\x96\xe7\xb3\xbb')]),
        ),
    ]
