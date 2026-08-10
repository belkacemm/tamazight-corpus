from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class CreateCorpusForm(FlaskForm):
    name = StringField(
        "Corpus name",
        validators=[
            DataRequired(),
            Length(min=2, max=100),
        ],
    )

    language = StringField(
        "Language",
        validators=[
            DataRequired(),
            Length(min=2, max=50),
        ],
    )

    submit = SubmitField("Create Corpus")