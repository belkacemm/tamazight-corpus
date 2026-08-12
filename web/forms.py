from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length
from wtforms.validators import Optional


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
class CreateSpeakerForm(FlaskForm):
    speaker_id = StringField(
        "Speaker ID",
        validators=[DataRequired()],
    )

    name = StringField(
        "Name",
        validators=[Optional()],
    )

    submit = SubmitField("Create Speaker")    