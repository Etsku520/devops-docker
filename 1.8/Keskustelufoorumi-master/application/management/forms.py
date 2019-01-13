from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, validators
from wtforms.widgets import TextArea

class CategoryForm(FlaskForm):
    name = StringField("name", [validators.Length(min=3)])

    class Meta:
        csrf = False