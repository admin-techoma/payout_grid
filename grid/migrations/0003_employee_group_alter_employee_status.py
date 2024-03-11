# Generated by Django 4.2.7 on 2024-03-09 21:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('grid', '0002_employee'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='auth.group'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='status',
            field=models.CharField(blank=True, choices=[('Active', 'Active'), ('Deactive', 'Deactive')], default='Activate', max_length=100, null=True),
        ),
    ]
