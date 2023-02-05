from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField, PasswordField


class FormularioJogo(FlaskForm):
    nome = StringField('Nome', [validators.DataRequired(), validators.Length(min=1, max=50)])
    categoria = StringField('Cpf', [validators.DataRequired(), validators.Length(min=1, max=40)])
    console = StringField('Email', [validators.DataRequired(), validators.Length(min=1, max=20)])
    salvar = SubmitField('Salvar')


class FormularioUsuario(FlaskForm):
    nickname = StringField('Nickname', [validators.DataRequired(), validators.Length(min=1, max=8)])
    senha = PasswordField('Senha', [validators.DataRequired(), validators.Length(min=1, max=100)])
    login = SubmitField('Login')
