# Generated by Django 4.2.7 on 2023-12-24 16:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_rename_initial_deposite_date_userbankaccount_initial_deposit_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userbankaccount',
            old_name='initial_deposit_date',
            new_name='initial_deposite_date',
        ),
    ]