from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange


class FacturacionForm(FlaskForm):
    cliente = StringField(
        'Nombre del cliente',
        validators=[DataRequired(message='El nombre del cliente es obligatorio.'),
                    Length(min=3, max=100, message='Debe tener entre 3 y 100 caracteres.')]
    )
    total = DecimalField(
        'Total ($)',
        places=2,
        validators=[DataRequired(message='El total es obligatorio.'),
                    NumberRange(min=0.01, message='El total debe ser mayor a 0.')]
    )
    estado = SelectField(
        'Estado',
        choices=[
            ('Pendiente', 'Pendiente'),
            ('Pagada', 'Pagada'),
            ('Anulada', 'Anulada')
        ],
        validators=[DataRequired(message='Selecciona un estado.')]
    )
    submit = SubmitField('Registrar factura')