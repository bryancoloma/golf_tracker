from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.paint import Paint
from flask_app.models.user import User