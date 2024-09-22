from django.db import models

# Create your models here.


class Clientes(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=11, blank=True, null=True)
    data_nascimento = models.DateField()
    telefone = models.CharField(max_length=11)
    data_criacao = models.DateTimeField(auto_now_add=True)
    renda_mensal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nome


class Emprestimos(models.Model):
    cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_emprestimo = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Emprestimo de {self.valor} para {self.cliente.nome}"


class Cartao_de_credito(models.Model):
    cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE)
    limite = models.DecimalField(max_digits=10, decimal_places=2)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cartão de crédito de {self.cliente.nome}"
