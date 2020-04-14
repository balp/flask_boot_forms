import json
import os
from dataclasses import dataclass, asdict
from random import randrange
from typing import Optional

from flask import Flask, render_template
from flask_wtf.csrf import CSRFProtect
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField
from wtforms.validators import DataRequired, NumberRange

MAX_NUMBER = 6


def create_app():
    new_app = Flask(__name__)
    new_app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    CSRFProtect(new_app)
    Bootstrap(new_app)
    return new_app


app: Flask = create_app()
name: Optional[str] = None
target: int = randrange(MAX_NUMBER)
hit_count: int = 0


class MyForm(FlaskForm):
    target = DecimalField('target', validators=[DataRequired(), NumberRange(0, MAX_NUMBER)])


@app.route('/', methods=['GET', 'POST'])
def index():
    global name
    form = MyForm()
    if form.validate_on_submit():
        name = form.name.data
        global target
        target = int(form.target.data)
        return render_template('index.html',
                               target=target,
                               range=str(MAX_NUMBER),
                               form=form)
    return render_template('index.html',
                           target=target,
                           range=str(MAX_NUMBER),
                           form=form)


@dataclass
class RandomCounter:
    random: int
    hits: int


@app.route('/random', methods=['GET'])
def random():
    global hit_count
    random_number = randrange(MAX_NUMBER)
    if random_number == target:
        hit_count += 1
    rnd = RandomCounter(random_number, hit_count)
    return json.dumps(asdict(rnd))


if __name__ == '__main__':
    app.run()
