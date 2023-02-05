from models import Jogos
from flask import flash
from re import search


def acha_tamanho(numero):
    numero = abs(int(numero))
    if numero < 2:
        return 1
    count = 0
    valor = 1
    while valor <= numero:
        valor *= 10
        count += 1
    return count


def validar(cpf):
    resultado = []
    while True:
        if acha_tamanho(cpf) != 11:
            return '!=11'
        if acha_tamanho(cpf) == 11:
            break
    valor1 = int(cpf[0]) * 10
    valor2 = int(cpf[1]) * 9
    valor3 = int(cpf[2]) * 8
    valor4 = int(cpf[3]) * 7
    valor5 = int(cpf[4]) * 6
    valor6 = int(cpf[5]) * 5
    valor7 = int(cpf[6]) * 4
    valor8 = int(cpf[7]) * 3
    valor9 = int(cpf[8]) * 2
    soma1 = valor1 + valor2 + valor3 + valor4 + valor5 + valor6 + valor7 + valor8 + valor9
    res1 = (soma1 * 10) % 11
    if res1 == 10:
        res1 = 0
    if res1 == int(cpf[9]):
        resultado.append('2Válido')
    valor10 = int(cpf[0]) * 11
    valor11 = int(cpf[1]) * 10
    valor12 = int(cpf[2]) * 9
    valor13 = int(cpf[3]) * 8
    valor14 = int(cpf[4]) * 7
    valor15 = int(cpf[5]) * 6
    valor16 = int(cpf[6]) * 5
    valor17 = int(cpf[7]) * 4
    valor18 = int(cpf[8]) * 3
    valor19 = int(cpf[9]) * 2
    soma2 = valor10 + valor11 + valor12 + valor13 + valor14 + valor15 + valor16 + valor17 + valor18 + valor19
    res2 = (soma2 * 10) % 11
    if res2 == 10:
        res2 = 0
    if res2 == int(cpf[10]):
        resultado.append('3Válido')
    if '2Válido' and '3Válido' in resultado:
        return True
    else:
        return False


def verifica_se_email_eh_valido(email):
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if search(regex, email):
        return True
    else:
        return False


def validando_nome_cpf_email(nome, cpf, email):
    lista = ['nome', 'cpf', 'email']

    # Verificando NOME
    jogo = Jogos.query.filter_by(nome=nome).first()
    if jogo:
        flash('Nome já cadastrado!')
    else:
        lista.remove('nome')

    # Verificando CPF
    if validar(cpf) == '!=11':
        flash('O número de CPF deve ter 11 dígitos')
    if not validar(cpf):
        flash('CPF inválido')

    jogo = Jogos.query.filter_by(categoria=cpf).first()
    if validar(cpf):
        if jogo:
            flash('CPF já cadastrado!')
        else:
            lista.remove('cpf')

    # Verificando EMAIL
    jogo = Jogos.query.filter_by(console=email).first()
    if not verifica_se_email_eh_valido(email):
        flash('Email inválido!')
    else:
        if jogo:
            flash('Email já cadastrado!')
        else:
            lista.remove('email')

    # Verificação geral
    if 'nome' not in lista:
        if 'cpf' not in lista:
            if 'email' not in lista:
                flash('Cadastro realizado com sucesso!')
                return True
            else:
                return False
