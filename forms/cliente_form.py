from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email


class ClienteForm(FlaskForm):
    nombre = StringField(
        'Nombre completo',
        validators=[DataRequired(message='El nombre es obligatorio.'),
                    Length(min=3, max=100, message='Debe tener entre 3 y 100 caracteres.')]
    )
    correo = StringField(
        'Correo electrónico',
        validators=[DataRequired(message='El correo es obligatorio.'),
                    Email(message='Ingresa un correo electrónico válido.')]
    )
    telefono = StringField(
        'Teléfono',
        validators=[DataRequired(message='El teléfono es obligatorio.'),
                    Length(min=7, max=10, message='Debe tener entre 7 y 10 dígitos.')]
    )
    direccion = StringField(
        'Dirección',
        validators=[DataRequired(message='La dirección es obligatoria.'),
                    Length(min=5, max=200, message='Debe tener entre 5 y 200 caracteres.')]
    )
    activo = BooleanField('Cliente activo', default=True)
    submit = SubmitField('Guardar cliente')