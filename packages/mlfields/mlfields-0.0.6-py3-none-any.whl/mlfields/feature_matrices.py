from flask import (
    Blueprint,
    render_template,
    url_for
)

from mlfields.data_models import (
    Projects,
    FeatureMatrices
)


bp = Blueprint('feature_matrices', __name__)

@bp.route('', methods=('GET',))
def list(project_id):
    project = Projects.query.filter_by(project_id=project_id).first()
    fms = FeatureMatrices.query.filter_by(project_id=project_id)
    urls = [url_for("feature_evaluations.list", project_id=project.project_id, fm_id=fm.fm_id) for fm in fms]
    return render_template('feature_matrices/list.html', project=project, contexts=zip(fms, urls))
