from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, validators, SelectField
from wtforms.widgets import TextArea

class GroupForm(FlaskForm):
    heading = StringField("Heading", [validators.Length(min=4)])
    class Meta:
        csrf = False

class GroupcategoryFrom(FlaskForm):
    category = SelectField("Category")

    class Meta:
        csrf = False