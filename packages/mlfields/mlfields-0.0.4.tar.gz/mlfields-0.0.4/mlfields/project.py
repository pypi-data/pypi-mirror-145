from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for
)

from mlfields.data_models import (
    db,
    Projects
)


bp = Blueprint('projects', __name__)


@bp.route('/projects/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        name = request.form['name']
        note = request.form['note']
        error = None
        if not name:
            error = 'Name is required.'
        if error is not None:
            flash(error)
        else:
            new_project = Projects(name=name, note=note)
            db.session.add(new_project)
            db.session.commit()
            return redirect(url_for("projects.list"))
    return render_template('projects/create.html')


@bp.route('/projects/', methods=('GET',))
def list():
    projects = Projects.query
    urls = [url_for("feature_matrices.list", project_id=p.project_id) for p in projects]
    return render_template('projects/list.html', contexts=zip(projects, urls))


@bp.route('/', methods=('GET',))
def index():
    return redirect(url_for('projects.list'))
