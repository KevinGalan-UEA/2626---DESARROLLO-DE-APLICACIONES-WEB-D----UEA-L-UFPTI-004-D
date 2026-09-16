from flask_wtf import FlaskForm
from wtforms import SelectField, DecimalField, SubmitField
from wtforms.validators import DataRequired, NumberRange


class FacturacionForm(FlaskForm):
    id_cliente = SelectField(
        'Cliente',
        coerce=int,
        validators=[DataRequired(message='Selecciona un cliente.')]
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