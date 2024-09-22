from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Clientes, Emprestimos, Cartao_de_credito
from datetime import datetime, date
from django.http import JsonResponse
from django.views.decorators.http import require_POST


def index(request):
    if request.method == 'POST':
        usuario = request.POST.get('usuario')
        senha = request.POST.get('senha')
        if usuario == 'admin' and senha == 'admin':
            return redirect('pagina_inicial')
        messages.error(request, 'Usuário ou senha inválidos')
    return render(request, 'index.html')


def pagina_inicial(request):
    clientes = Clientes.objects.all()
    return render(request, 'pagina_inicial.html', {'clientes': clientes})


def cadastrar_cliente(request):
    nome = request.POST.get('nome').strip()
    if any(char.isdigit() for char in nome):
        messages.error(request, 'O nome não pode conter números')
        return redirect('pagina_inicial')
    cpf = request.POST.get('cpf').strip()
    if any(char.isalpha() for char in cpf):
        messages.error(request, 'O CPF não pode conter letras')
        return redirect('pagina_inicial')
    data_nascimento = request.POST.get('data_nascimento')
    data_nascimento_formatada = datetime.strptime(
        data_nascimento, '%Y-%m-%d').date()
    data_atual = datetime.now().date()
    idade = data_atual.year - data_nascimento_formatada.year
    if (data_atual.month, data_atual.day) < (data_nascimento_formatada.month, data_nascimento_formatada.day):
        idade -= 1
    if idade < 12:
        messages.error(
            request, 'Cliente menor de 12 anos não pode criar conta')
        return redirect('pagina_inicial')
    telefone = request.POST.get('telefone').strip()
    renda_mensal = request.POST.get('renda_mensal')
    cliente = Clientes(nome=nome, cpf=cpf, data_nascimento=data_nascimento,
                       telefone=telefone, renda_mensal=renda_mensal)
    cliente.save()
    messages.success(request, 'Cliente cadastrado com sucesso')
    return redirect('pagina_inicial')


def deletar_cliente(request, id):
    cliente = Clientes.objects.get(id=id)
    cliente.delete()
    messages.success(request, 'Cliente deletado com sucesso')
    return redirect('pagina_inicial')


@require_POST
def realizar_emprestimo(request, id):
    cliente = Clientes.objects.get(id=id)
    if cliente.cpf == '' or cliente.cpf is None:
        messages.error(request, 'CPF do cliente não informado')
        return redirect('pagina_inicial')
    idade = (datetime.now().date() - cliente.data_nascimento).days // 365
    if idade < 18:
        messages.error(request, 'Cliente menor de 18 anos')
        return redirect('pagina_inicial')
    valor = float(request.POST.get('valor', 0))
    renda_mensal = float(cliente.renda_mensal)
    if renda_mensal <= 4999:
        if valor > 2500:
            messages.error(
                request, 'Crédito liberado de até R$ 2.500,00 para renda mensal de até R$ 4.999,00')
            return redirect('pagina_inicial')
        else:
            messages.success(request, 'Empréstimo realizado com sucesso')
            return redirect('pagina_inicial')
    elif 5000 <= renda_mensal <= 10000:
        if valor > 5000:
            messages.error(
                request, 'Crédito liberado de até R$ 5.000,00 para renda mensal de até R$ 10.000,00')
            return redirect('pagina_inicial')
        else:
            messages.success(request, 'Empréstimo realizado com sucesso')
            return redirect('pagina_inicial')
    elif renda_mensal > 10000:
        if valor > 10000:
            messages.error(
                request, 'Crédito liberado de até R$ 10.000,00 para renda mensal acima de R$ 10.000,00')
            return redirect('pagina_inicial')
        else:
            messages.success(request, 'Empréstimo realizado com sucesso')
            return redirect('pagina_inicial')
    emprestimo = Emprestimos(cliente=cliente, valor=valor)
    emprestimo.save()
    messages.success(request, 'Empréstimo realizado com sucesso')
    return redirect('pagina_inicial')


def editar_cliente(request, id):
    cliente = Clientes.objects.get(id=id)
    nome = request.POST.get('nome')
    cpf = request.POST.get('cpf')
    data_nascimento = request.POST.get('data_nascimento')
    telefone = request.POST.get('telefone')
    renda_mensal = request.POST.get('renda_mensal')
    cliente.nome = nome
    cliente.cpf = cpf
    cliente.data_nascimento = data_nascimento
    cliente.telefone = telefone
    cliente.renda_mensal = renda_mensal
    cliente.save()
    messages.success(request, 'Cliente atualizado com sucesso')
    return redirect('pagina_inicial')


def get_cliente_data(request, id):
    try:
        cliente = Clientes.objects.get(id=id)
        return JsonResponse({
            'nome': cliente.nome,
            'cpf': cliente.cpf,
            'data_nascimento': cliente.data_nascimento.strftime('%Y-%m-%d'),
            'telefone': cliente.telefone,
            'renda_mensal': cliente.renda_mensal
        })
    except Clientes.DoesNotExist:
        return JsonResponse({'error': 'Cliente não encontrado'}, status=404)


def cadastrar_cartao_de_credito(request, id):
    cliente = Clientes.objects.get(id=id)
    if cliente.cpf == '' or cliente.cpf is None:
        messages.error(request, 'CPF do cliente não informado')
        return redirect('pagina_inicial')
    limite = float(request.POST.get('limite'))
    if limite == '' or limite is None:
        messages.error(request, 'Limite do cartão não informado')
        return redirect('pagina_inicial')
    if cliente.renda_mensal < 1350:
        messages.error(request, 'Renda mensal menor que o minimo para credito')
        return redirect('pagina_inicial')
    elif cliente.renda_mensal >= 1350 and cliente.renda_mensal <= 5000:
        if limite < 2500 or limite > 5000:
            messages.error(
                request, 'Valor de credito deve ser entre R$ 2.500,00 e R$ 5.000,00')
            return redirect('pagina_inicial')
        else:
            messages.success(
                request, 'Cartão de crédito cadastrado com sucesso')
            return redirect('pagina_inicial')
    elif cliente.renda_mensal >= 5000 and cliente.renda_mensal <= 10000:
        if limite < 5000 or limite > 10000:
            messages.error(
                request, 'Valor de credito deve ser entre R$ 5.000,00 e R$ 10.000,00')
            return redirect('pagina_inicial')
        else:
            messages.success(
                request, 'Cartão de crédito cadastrado com sucesso')
            return redirect('pagina_inicial')
    elif cliente.renda_mensal > 10000:
        if limite < 10000 or limite > 20000:
            messages.error(
                request, 'Valor de credito deve ser entre R$ 10.000,00 e R$ 20.000,00')
            return redirect('pagina_inicial')

        else:
            messages.success(
                request, 'Cartão de crédito cadastrado com sucesso')
            return redirect('pagina_inicial')
    cartao_de_credito = Cartao_de_credito(cliente=cliente, limite=limite)

    cartao_de_credito.save()
    messages.success(request, 'Cartão de crédito cadastrado com sucesso')
    return redirect('pagina_inicial')
