from flask import render_template, request, redirect, session, flash, url_for
from jogoteca import app, db
from models import Jogos
from helpers import FormularioJogo
from codigo import validando_nome_cpf_email
from helpers import FormularioUsuario


@app.route('/')
def login():
    proxima = request.args.get('proxima')
    form = FormularioUsuario()
    return render_template('login.html', proxima=proxima, form=form)


@app.route('/lista')
def index():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('index')))
    lista = Jogos.query.order_by(Jogos.id)
    return render_template('lista.html', titulo='Cadastros', jogos=lista)


@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    form = FormularioJogo(request.form)
    return render_template('novo.html', titulo='Novo Cadastro', form=form)


@app.route('/criar', methods=['POST', ])
def criar():
    form = FormularioJogo(request.form)

    if not form.validate_on_submit():
        return redirect(url_for('novo'))

    nome = form.nome.data
    cpf = form.categoria.data
    email = form.console.data

    if validando_nome_cpf_email(nome, cpf, email):
        novo_jogo = Jogos(nome=nome, categoria=cpf, console=email)
        db.session.add(novo_jogo)
        db.session.commit()
        return redirect(url_for('index'))
    else:
        novo_jogo = Jogos(nome=nome, categoria=cpf, console=email)
        db.session.add(novo_jogo)
        db.session.commit()
        return redirect(url_for('editar', id=novo_jogo.id))


@app.route('/atualizar', methods=['POST', ])
def atualizar():
    form = FormularioJogo(request.form)
    jogo = Jogos.query.filter_by(id=request.form['id']).first()

    if form.validate_on_submit():
        if validando_nome_cpf_email(nome=form.nome.data, cpf=form.categoria.data, email=form.console.data):
            jogo.nome = form.nome.data
            jogo.categoria = form.categoria.data
            jogo.console = form.console.data
            db.session.add(jogo)
            db.session.commit()
            return redirect(url_for('index'))
        else:
            return redirect(url_for('editar', id=jogo.id))


@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('editar', id=id)))

    jogo = Jogos.query.filter_by(id=id).first()
    form = FormularioJogo()
    form.nome.data = jogo.nome
    form.categoria.data = jogo.categoria
    form.console.data = jogo.console
    return render_template('editar.html', titulo='Editando Cadastro', id=id, form=form)


@app.route('/deletar/<int:id>')
def deletar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))

    Jogos.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Cadastro deletado com sucesso')
    return redirect(url_for('index'))
