from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class SearchSeatFrom(FlaskForm):
	name = StringField('查找的座位号或者姓名是？', validators=[DataRequired()])
	search = SubmitField('查找')