#coding=utf-8

from flask import Blueprint

blueprint = Blueprint('images', __name__)

from . import views
