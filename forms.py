import email
from wtforms import BooleanField, StringField, PasswordField, validators , ValidationError, HiddenField,FloatField,IntegerField,SubmitField,SelectField,SelectMultipleField,TextAreaField,FileField,Form,DateTimeField
from flask_wtf import FlaskForm, Form
from wtforms.fields.html5 import DateField
from flask_wtf.file import FileField,FileRequired,FileAllowed

class Addmeme(Form):
    tags = StringField('Tags', [validators.DataRequired()])
    type = SelectField('Status', choices=[('picture','picture'),('video','video'),('gif','gif')])
    # status = StringField('Status', default=True)
    # rivacy = SelectField('Display', choices=[('yes','Yes'),('no','No')])   
    image_1 = FileField('Image 1', validators=[FileRequired(), FileAllowed(['jpg','png','gif','jpeg'])])
    submit = SubmitField('SUBMIT')