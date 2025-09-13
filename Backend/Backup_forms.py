from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, PasswordField
from wtforms.validators import DataRequired, NumberRange, Length
from wtforms.widgets import TextInput
from wtforms.fields import DateField

class LoginForm(FlaskForm):
    username = StringField('Usuário', validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Entrar')

class PrecoField(StringField):
    def process_formdata(self, valuelist):
        if valuelist:
            try:
                self.data = float(valuelist[0].replace(',', '.'))
                if self.data < 0:
                    raise ValueError("O preço não pode ser negativo")
            except ValueError:
                self.data = None
                raise ValueError("Digite um valor válido (exemplo: 5,99")

class ProdutoForm(FlaskForm):
    nome = StringField('Nome do Produto', validators=[DataRequired()])
    quantidade = IntegerField('Quantidade', validators=[DataRequired(), NumberRange(min=1, message="A quantidade deve ser maior que 0.")])
    preco = PrecoField('Preço (R$)', validators=[DataRequired()], widget=TextInput())
    validade = DateField('Validade', format = '%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Adicionar Produto')