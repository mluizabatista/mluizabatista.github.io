from site.jogoteca import app
from flask import request, redirect, session, flash, url_for
from site.models import Usuarios
from site.helpers import FormularioUsuario
from flask_bcrypt import check_password_hash


@app.route('/autenticar', methods=['POST', ])
def autenticar():
    form = FormularioUsuario(request.form)

    usuario = Usuarios.query.filter_by(nickname=form.nickname.data).first()
    senha = check_password_hash(usuario.senha, form.senha.data)
    if usuario and senha:
        session['usuario_logado'] = usuario.nickname
        flash(usuario.nickname + ' logado com sucesso!')
        proxima_pagina = request.form['proxima']
        return redirect(proxima_pagina)

    else:
        flash('Usuário não logado.')
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso!')
    return redirect(url_for('index'))
