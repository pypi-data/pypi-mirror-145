from flask import (
    Blueprint,
    render_template,
    url_for,
    request
)

from mlfields.data_models import (
    Projects,
    FeatureDefinitions
)


bp = Blueprint('feature_definitions', __name__)
@bp.route('', methods=('GET',))
def list(project_id):
    project = Projects.query.filter_by(project_id=project_id).first()
    fds = FeatureDefinitions.query.filter_by(project_id=project_id)
    return render_template('feature_definitions/list.html', project=project, fds=fds)
