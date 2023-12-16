# Generated by Django 4.2.8 on 2023-12-16 21:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Customer",
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
                ("first_name", models.CharField(max_length=50)),
                ("last_name", models.CharField(max_length=50)),
                ("age", models.IntegerField()),
                (
                    "monthly_salary",
                    models.DecimalField(decimal_places=2, max_digits=10),
                ),
                ("phone_number", models.CharField(max_length=15)),
                (
                    "approved_limit",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                (
                    "current_debt",
                    models.DecimalField(decimal_places=2, default=0, max_digits=10),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Loan",
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
                ("loan_id", models.CharField(max_length=50)),
                ("loan_amount", models.DecimalField(decimal_places=2, max_digits=10)),
                ("tenure", models.IntegerField()),
                ("interest_rate", models.DecimalField(decimal_places=2, max_digits=5)),
                (
                    "monthly_repayment",
                    models.DecimalField(decimal_places=2, max_digits=10),
                ),
                ("emis_paid_on_time", models.IntegerField()),
                ("start_date", models.DateField()),
                ("end_date", models.DateField()),
                (
                    "customer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="CAS.customer"
                    ),
                ),
            ],
        ),
    ]