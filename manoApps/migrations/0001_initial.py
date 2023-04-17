# Generated by Django 4.2 on 2023-04-13 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Asmenys",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "user_name",
                    models.CharField(
                        help_text="Įveskite savo Vardą",
                        max_length=80,
                        verbose_name="Vardas",
                    ),
                ),
                (
                    "user_surname",
                    models.CharField(
                        help_text="Įveskite savo Pavardę",
                        max_length=80,
                        verbose_name="Pavardė",
                    ),
                ),
                (
                    "user_birth_date",
                    models.DateField(
                        help_text="Įveskite savo gimimo datą",
                        verbose_name="Gimimo data",
                    ),
                ),
                ("age", models.IntegerField(verbose_name="Amžius")),
            ],
        ),
    ]
