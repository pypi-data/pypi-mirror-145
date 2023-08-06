import os
from os import environ

import click
from flask import (
    Flask,
    current_app
)
from flask.cli import with_appcontext
from flask_restful import Api


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    db_uri = environ.get("MLFIELDS_SQLALCHEMY_DATABASE_URI") or f'sqlite:///{app.instance_path}/mlfields.db'
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI = db_uri
    )

    if test_config:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/hello')
    def hello():
        return 'Hello, World'

    from .data_models import db
    db.init_app(app)
    add_init_db_command(app)

    from . import project
    app.register_blueprint(project.bp)

    from . import feature_matrices
    app.register_blueprint(feature_matrices.bp, url_prefix='/projects/<int:project_id>/fms/')

    from . import feature_definitions
    app.register_blueprint(feature_definitions.bp, url_prefix='/projects/<int:project_id>/fds/')

    from . import evaluation_metrics
    app.register_blueprint(evaluation_metrics.bp, url_prefix='/projects/<int:project_id>/metrics/')

    from . import feature_evaluations
    app.register_blueprint(feature_evaluations.bp, url_prefix='/projects/<int:project_id>/fms/<int:fm_id>/')

    from . import feature_evaluations_for_each_feature
    app.register_blueprint(feature_evaluations_for_each_feature.bp, url_prefix='/projects/<int:project_id>/fds/<int:feature_id>/')

    from .apis import (
        pjs,
        fds,
        fms,
        metrics,
        fes
    )
    api = Api(app)
    api.add_resource(pjs.PJs, '/api/projects/')
    api.add_resource(fds.FDs, '/api/projects/<int:project_id>/fds/')
    api.add_resource(fms.FMs, '/api/projects/<int:project_id>/fms/')
    api.add_resource(metrics.Metrics, '/api/projects/<int:project_id>/metrics/')
    api.add_resource(fes.FEs, '/api/projects/<int:project_id>/fms/<int:fm_id>/')

    return app


@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Initialized the database.')


def add_init_db_command(app):
    app.cli.add_command(init_db_command)


def init_db():
    from .data_models import db
    db = data_models.db
    with current_app.app_context():
        db.create_all()
