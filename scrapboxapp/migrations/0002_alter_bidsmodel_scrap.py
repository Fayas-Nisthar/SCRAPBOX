# Generated by Django 4.2.7 on 2024-01-20 10:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scrapboxapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bidsmodel',
            name='scrap',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bid_scrap', to='scrapboxapp.scrapmodel'),
        ),
    ]
