from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, validators, SelectField
from wtforms.widgets import TextArea

class MessageForm(FlaskForm):
    name = TextAreaField("Message", [validators.Length(min=1)], widget=TextArea())

    class Meta:
        csrf = False
