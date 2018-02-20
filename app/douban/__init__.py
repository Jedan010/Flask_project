from flask import Blueprint

douban = Blueprint('douban', __name__)

from .import views
