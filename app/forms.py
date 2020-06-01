# Flask WTF
from flask_wtf import FlaskForm
from wtforms.fields import StringField
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
    """[Class that represents the product search form]

    Arguments:
        FlaskForm {[type]} -- [Extends from the FlaskForm class]
    """
    search = StringField('', validators=[DataRequired()])
