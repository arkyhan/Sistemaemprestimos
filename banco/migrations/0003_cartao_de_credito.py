# Generated by Django 5.1.1 on 2024-09-21 18:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banco', '0002_alter_clientes_cpf_emprestimos'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cartao_de_credito',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('limite', models.DecimalField(decimal_places=2, max_digits=10)),
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='banco.clientes')),
            ],
        ),
    ]
