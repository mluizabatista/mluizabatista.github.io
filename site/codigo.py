from re import search
from models import Jogos
from flask import flash
from verificador_de_cpf import validar


def titulo(msg):
    print('=='*20)
    print(msg.center(40))
    print('=='*20)


def recarregar():
    topicos()
    carregar_opcoes()


def criar_arquivo():
    try:
        a = open('../outros/Arquivos/banco_de_dados.txt', 'wt+')
        a.close()
    except FileNotFoundError:
        print('Banco de dados não encontrado')
    else:
        print('Banco de dados encontrado')


def se_arquivo_existe():
    try:
        a = open('../outros/Arquivos/banco_de_dados.txt', 'rt')
        a.close()
    except FileNotFoundError:
        return False
    else:
        return True


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


'''
def validar(cpf):
    resultado = []
    while True:
        if acha_tamanho(cpf) != 11:
            print('ERRO! PREENCHA OS 11 DÍGITOS')
            cpf = input('Digite os números do CPF: ')
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
        print('CPF válido!')
        return True
    else:
        print('CPF inválido!')
        return False
'''


def topicos():
    titulo('Site Batista :)')
    opcoes = ['Ver banco de dados', 'Novo cadastro', 'Pesquisar no banco de dados', 'Sair']
    c = 1
    for item in opcoes:
        print(f'{c} - {item}')
        c += 1


def verifica_se_email_eh_valido(email):
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if search(regex, email):
        return True
    else:
        return False


def inserir_no_sistema(informacoes):
    a = open(f'../outros/Arquivos/banco_de_dados.txt', 'at')
    a.write(f'{informacoes["Nome"]:<20}{informacoes["Idade"]:<5}{informacoes["E-mail"]:<30}{informacoes["Cpf"]:<15}')
    a.write('\n')
    a.close()


def novo_cadastro():
    titulo('OPÇÃO 2 - Novo cadastro')
    informacoes = {'Nome': str(input('Nome: ')), 'Idade': int(input('Idade: '))}
    email = str(input('Digite o email: '))

    while True:
        if not verifica_se_email_eh_valido(email):
            email = str(input('Digite o email: '))
        else:
            break

    cpf = input('Digite os números do CPF: ')

    while True:
        if not validar(cpf):
            cpf = input('Digite os números do CPF: ')
        else:
            break

    if verifica_se_ja_eh_cadastrado_pelo_cpf_e_mostra_a_linha(cpf):
        informacoes['Cpf'] = cpf
        informacoes['E-mail'] = email
        inserir_no_sistema(informacoes)
        print('| CADASTRO COMPLETO |'.center(40))
    recarregar()


def ver_banco_de_dados():
    titulo('OPÇÃO 1 - Ver banco de dados')
    a = open('../outros/Arquivos/banco_de_dados.txt', 'rt')
    print(a.read())
    a.close()
    recarregar()


def verifica_se_ja_eh_cadastrado_pelo_cpf_e_mostra_a_linha(cpf):
    a = open("../outros/Arquivos/banco_de_dados.txt", "r")
    flag = 0
    index = 0
    for line in a:
        index += 1
        if cpf in line:
            flag = 1
            break
    a.close()
    if flag == 0:
        print('Cadastro não localizado')
        return True
    else:
        print('Cadastro localizado')
        with open("../outros/Arquivos/banco_de_dados.txt") as f:
            data = f.readlines()[index - 1]
        print('--'*20)
        print(data)
        print('--' * 20)
        return False


def pesquisar_no_banco_de_dados():
    titulo('OPÇÃO 3 - Pesquisar no banco de dados')
    cpf = str(input('Digite o e-mail ou CPF: '))
    verifica_se_ja_eh_cadastrado_pelo_cpf_e_mostra_a_linha(cpf)
    recarregar()


def carregar_opcoes():
    while True:
        opc = int(input('Digite uma das 4 opções: '))
        if opc == 1:
            ver_banco_de_dados()
            break
        elif opc == 2:
            novo_cadastro()
            break
        elif opc == 3:
            pesquisar_no_banco_de_dados()
            break
        elif opc == 4:
            print('=='*20)
            print('Saindo...')
            break
        else:
            print('Digite uma das 3 opções!')


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
