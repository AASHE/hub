# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-09-15 15:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('metadata', '0024_greenpowerfinanceoption_greenpowerinstallation_greenpowerlocation'),
        ('content', '0081_auto_20170720_2221'),
    ]

    operations = [
        migrations.CreateModel(
            name='GreenPowerProject',
            fields=[
                ('contenttype_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='content.ContentType')),
                ('project_size', models.CharField(max_length=50)),
                ('annual_production', models.CharField(blank=True, max_length=50, null=True)),
                ('installed_cost', models.CharField(blank=True, max_length=50, null=True)),
                ('ownership_type', models.CharField(choices=[(b'unknown', b'Unknown'), (b'institution-owned', b'Institution Owned'), (b'third-party-lease', b'Third-party owned (lease)'), (b'third-party-purchase', b'Third-party owned (power purchase agreement)')], max_length=200)),
                ('money_saver', models.CharField(blank=True, choices=[(b'yes', b'Yes'), (b'no', b'No'), (b'unknown', b'Unknown')], max_length=100, null=True)),
                ('cost_savings_desc', models.TextField(blank=True, null=True)),
                ('starting_ppa_price', models.CharField(blank=True, choices=[(b'< 3', b'<$0.03'), (b'4 - 4.9', b'$0.04-0.049'), (b'5 - 5.9', b'$0.05-0.059'), (b'6 - 6.9', b'$0.06-0.069'), (b'7 - 7.9', b'$0.07-0.079'), (b'8 - 8.9', b'$0.08-0.089'), (b'9 - 9.9', b'$0.09-0.099'), (b'10 - 10.9', b'$0.10-$0.109'), (b'11 - 11.9', b'$0.11-$0.119'), (b'> 12', b'>$12')], max_length=50, null=True)),
                ('ppa_escalator', models.CharField(blank=True, choices=[(b'0 (i.e., no annual escalator)', b'0 (i.e., no annual escalator)'), (b'0.01% to 1%', b'0.01% to 1%'), (b'1% to 1.49%', b'1% to 1.49%'), (b'1.5% to 1.99%', b'1.5% to 1.99%'), (b'2% to 2.49%', b'2% to 2.49%'), (b'2.5% to 2.99%', b'2.5% to 2.99%'), (b'3% to 4%', b'3% to 4%'), (b'Greater than 4%', b'Greater than 4%')], max_length=50, null=True)),
                ('ppa_escalator_desc', models.TextField(blank=True, null=True)),
                ('ppa_duration', models.PositiveIntegerField(blank=True, null=True)),
                ('finance_sources', models.ManyToManyField(blank=True, help_text=b'Select up to 3', to='metadata.GreenPowerFinanceOption', verbose_name=b'Source(s) of Financing')),
                ('installations', models.ManyToManyField(help_text=b'Select up to three', to='metadata.GreenPowerInstallation', verbose_name=b'Installation Type')),
                ('locations', models.ManyToManyField(help_text=b'Select up to 2', to='metadata.GreenPowerLocation', verbose_name=b'Project Location')),
            ],
            options={
                'verbose_name': 'Green Power Project',
                'verbose_name_plural': 'Green Power Projects',
            },
            bases=('content.contenttype',),
        ),
    ]