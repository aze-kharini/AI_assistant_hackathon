from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
# Since I had to install additional packages, I do not think that email validator will work on the server
from wtforms.validators import InputRequired

class QuestionForm(FlaskForm):
    Question = StringField("Question:", validators=[InputRequired()])
    Database_name = SelectField("Database name:", choices=["database_names"], validators=[InputRequired()])
    submit = SubmitField("Query")


