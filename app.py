import json
import logging
import os
from dataclasses import dataclass, asdict
from logging.config import dictConfig
from random import randrange
from typing import Optional

from flask import Flask, render_template, request, has_request_context
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import DecimalField
from wtforms.validators import DataRequired, NumberRange

MAX_NUMBER = 6


class CriticalErrorWarningFilter(logging.Filter):
    def __init__(self, param=None):
        super().__init__()
        self.param = param

    def filter(self, record: logging.LogRecord):
        allow = record.levelno >= logging.WARNING
        return allow


class InfoDebugFilter(logging.Filter):
    def __init__(self, param=None):
        super().__init__()
        self.param = param

    def filter(self, record: logging.LogRecord):
        allow = record.levelno < logging.WARNING
        return allow


class RequestFormatter(logging.Formatter):
    def format(self, record):
        if has_request_context():
            record.url = request.url
            record.remote_addr = request.remote_addr
            record.trace = request.headers.get('X-Cloud-Trace-Context')
        else:
            record.url = None
            record.remote_addr = None
            record.trace = None

        return super().format(record)


dictConfig({
    'version': 1,
    'formatters': {'default': {
        '()': RequestFormatter,
        'format': '[%(asctime)s] %(remote_addr)s %(url)s %(trace)s %(levelname)s in %(module)s: %(message)s',
    }},
    'filters': {
        'warn_error_critical': {'()': CriticalErrorWarningFilter, },
        'info_debug': {'()': InfoDebugFilter, },
    },
    'handlers': {
        'wsgi_error': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'filters': ['warn_error_critical'],
            'formatter': 'default'
        },
        'wsgi_debug': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'filters': ['info_debug'],
            'formatter': 'default'
        },
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['wsgi_error', 'wsgi_debug']
    }
})


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
    app.logger.debug('index(): enter')
    app.logger.info('index(): enter')
    app.logger.warning('index(): enter')
    app.logger.error('index(): enter')
    app.logger.critical('index(): enter')
    form = MyForm()
    if form.validate_on_submit():
        global target
        target = int(form.target.data)
        app.logger.debug('index(): target: %s', target)
        return render_template('index.html',
                               target=target,
                               range=str(MAX_NUMBER),
                               form=form)
    app.logger.debug('index(): no form data')
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
    app.logger.info('random(): enter')
    app.logger.warning("warning")
    app.logger.error("error")
    random_number = randrange(MAX_NUMBER)
    if random_number == target:
        hit_count += 1
    rnd = RandomCounter(random_number, hit_count)
    return json.dumps(asdict(rnd))


if __name__ == '__main__':
    app.run()
