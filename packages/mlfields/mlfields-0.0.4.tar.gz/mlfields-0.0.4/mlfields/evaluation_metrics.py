from flask import (
    Blueprint,
    render_template,
    url_for
)
import pandas

from mlfields.data_models import (
    Projects,
    EvaluationMetrics
)


bp = Blueprint('evaluation_metrics', __name__)


@bp.route('', methods=('GET',))
def list(project_id):
    project = Projects.query.filter_by(project_id=project_id).first()
    metrics = EvaluationMetrics.query.filter_by(project_id=project_id)
    metric_df = pandas.read_sql(metrics.statement, metrics.session.bind)
    return render_template(
        'feature_evaluations/list_metrics.html', 
        project=project,  metric_df=metric_df
    )
