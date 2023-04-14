# Generated by Django 4.2 on 2023-04-13 22:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Consumer',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('street', models.CharField(max_length=255)),
                ('status', models.CharField(choices=[('collected', 'collected'), ('in_progress', 'in_progress'), ('active', 'active')], max_length=20)),
                ('previous_jobs_count', models.IntegerField()),
                ('amount_due', models.IntegerField()),
                ('lat', models.DecimalField(decimal_places=6, max_digits=9)),
                ('lng', models.DecimalField(decimal_places=6, max_digits=9)),
            ],
        ),
    ]