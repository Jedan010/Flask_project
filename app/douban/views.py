from flask import render_template
from . import douban
import pandas as pd
from .. import db



@douban.route('/movie')
def movie():
	Nowplaying = pd.read_sql_table('NowPlaying', db.engine).sort_values('score', ascending=False)
	Upcoming = pd.read_sql_table('Upcoming', db.engine)
	Upcoming.release_date = Upcoming.release_date.apply(
		lambda x: pd.to_datetime('2018/' + x[:-2].replace('月', '/').replace('日', '')))
	Upcoming.sort_values('release_date', inplace=True)
	return render_template('douban/movie.html', Nowplaying=Nowplaying, Upcoming=Upcoming)