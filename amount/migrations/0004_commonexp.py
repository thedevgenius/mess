# Generated by Django 4.2.4 on 2023-10-08 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('amount', '0003_remove_exp_amount_exp_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommonExp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('electric', models.IntegerField()),
                ('rice', models.IntegerField()),
                ('coock', models.IntegerField()),
            ],
        ),
    ]