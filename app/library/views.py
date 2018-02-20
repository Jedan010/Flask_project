from flask import render_template, session
from . import library
from .forms import SearchSeatFrom
import pandas as pd
from .. import db
import re

from flask import redirect, url_for, flash


@library.route('/seat', methods=['GET', 'POST'])
def seat():
	form = SearchSeatFrom()
	if form.validate_on_submit():
		name = form.name.data
		if name is not None:
			Seat = pd.read_sql_table('LibSeat', db.engine)
			search_seat = None
			if re.match('\d[a-fA-F]\d{3}', name):
				search_seat = Seat.loc[Seat['座位号'] == name.upper()]
			elif re.match(r"[\u4e00-\u9fa5]+", name):
				search_seat = Seat.loc[Seat['姓名'] == name]
			else:
				flash('输入信息有误！')
			if isinstance(search_seat, pd.DataFrame) and not search_seat.empty:
				return render_template('library/seat_result.html', form=form, search_seat = search_seat.iloc[0,1:].to_dict())
			elif isinstance(search_seat, pd.DataFrame) and search_seat.empty:
				flash('查询的用户或者座位暂时未选座')
	return render_template('library/seat.html', form=form)
