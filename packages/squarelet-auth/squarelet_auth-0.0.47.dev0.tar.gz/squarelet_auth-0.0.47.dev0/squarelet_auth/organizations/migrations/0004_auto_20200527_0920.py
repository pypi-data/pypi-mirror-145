# Generated by Django 2.0.8 on 2020-05-27 09:20

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('squarelet_auth_organizations', '0003_plan_resources'),
    ]

    operations = [
        migrations.CreateModel(
            name='Entitlement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='name')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='slug')),
                ('description', models.TextField()),
                ('resources', django.contrib.postgres.fields.jsonb.JSONField(default=dict)),
            ],
        ),
        migrations.AddField(
            model_name='organization',
            name='entitlement',
            field=models.ForeignKey(help_text='The subscription type for this organization', null=True, on_delete=django.db.models.deletion.PROTECT, to='squarelet_auth_organizations.Entitlement', verbose_name='entitlement'),
        ),
    ]
