import os
from typing import Optional

from flask import Flask, render_template, redirect
from flask_wtf.csrf import CSRFProtect
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


def create_app():
    new_app = Flask(__name__)
    new_app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    CSRFProtect(new_app)
    Bootstrap(new_app)
    return new_app


app: Flask = create_app()
name: Optional[str] = None


class MyForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])


@app.route('/', methods=('GET', 'POST'))
def index():
    global name
    form = MyForm()
    if form.validate_on_submit():
        name = form.name.data
        return render_template('index.html', name=name, form=form)
    return render_template('index.html', name=name, form=form)


if __name__ == '__main__':
    app.run()
