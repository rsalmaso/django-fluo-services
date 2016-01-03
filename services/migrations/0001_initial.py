# -*- coding: utf-8 -*-

# Copyright (C) 2007-2016, Raffaele Salmaso <raffaele@salmaso.org>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from __future__ import unicode_literals
from django.db import migrations, models
import fluo.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=255, null=True, verbose_name='name', blank=True)),
                ('email', models.EmailField(max_length=255, verbose_name='email')),
            ],
            options={
                'verbose_name': 'Service email',
                'verbose_name_plural': 'Service email',
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('status', fluo.db.models.fields.StatusField(max_length=10, verbose_name='status', choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active', help_text='Is active?')),
                ('ordering', fluo.db.models.fields.OrderField(verbose_name='ordering', default=0, help_text='Ordered', blank=True)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('slug', models.SlugField(editable=False, max_length=255, verbose_name='slug', help_text='A "slug" is a unique URL-friendly title for the object automatically generated from the "name" field.', unique=True)),
                ('default', models.BooleanField(verbose_name='default', default=False, help_text='Is the default one?')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Service',
                'verbose_name_plural': 'Services',
            },
        ),
        migrations.AddField(
            model_name='email',
            name='service',
            field=models.ForeignKey(verbose_name='service', to='services.Service', related_name='emails'),
        ),
        migrations.AlterUniqueTogether(
            name='email',
            unique_together=set([('service', 'email')]),
        ),
    ]
