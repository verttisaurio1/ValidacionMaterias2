# Generated by Django 4.1.2 on 2022-12-12 02:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ValidacionMaterias', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='registroequivalenciacomparativa',
            name='idPlanEstudioCarreraMateriaDE',
        ),
        migrations.AddField(
            model_name='registroequivalenciacomparativa',
            name='idMateriaA',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='registroequivalenciacomparativa',
            name='idMateriaDe',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]