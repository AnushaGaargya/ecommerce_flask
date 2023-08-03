from flask_wtf.file import FileField, FileAllowed,FileRequired
from wtforms import Form,IntegerField, StringField, BooleanField, DateField,TextAreaField, validators,DecimalField

class Addproducts(Form):
    name = StringField('Name',[validators.DataRequired(message=None)] )
    price = DecimalField('Price', [validators.DataRequired(message=None)])
    stock = IntegerField('Stock', [validators.DataRequired(message=None)])
    description = TextAreaField('Description', [validators.DataRequired(message=None)])
    mftr_date = DateField('Date of Manufacture', [validators.DataRequired(message=None)])
    exp_date = DateField('Date of Expiry', [validators.DataRequired(message=None)])
    
    # colors = TextAreaField('Colors', [validators.DataRequired()])

    image_1 = FileField('Image 1', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'gif', 'jpeg'])])
    