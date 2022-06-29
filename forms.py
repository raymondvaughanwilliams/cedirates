import email
from wtforms import BooleanField, StringField, PasswordField, validators , ValidationError, HiddenField,FloatField,IntegerField,SubmitField,SelectField,SelectMultipleField,TextAreaField,FileField,Form,DateTimeField
from flask_wtf import FlaskForm, Form
from wtforms.fields.html5 import DateField
from flask_wtf.file import FileField,FileRequired,FileAllowed

class Addmeme(Form):
    tags = StringField('Tags', [validators.DataRequired()])
    type = SelectField('Type', choices=[('picture','picture'),('video','video'),('gif','gif')])
    # status = StringField('Status', default=True)
    # rivacy = SelectField('Display', choices=[('yes','Yes'),('no','No')])   
    image_1 = FileField('Image 1', validators=[FileRequired(), FileAllowed(['jpg','png','gif','jpeg','mp4','webm'], 'jpg,png,gif,jpeg,mp4,webm only!')])
    submit = SubmitField('Add')



class Searchform(Form):
    search = StringField('Search', render_kw={"placeholder": "Search"})
    submit = SubmitField('Search',render_kw={"class": "fas fa-search"})