from flask import (
    Blueprint,
    render_template,
    url_for
)
import pandas

from mlfields.data_models import (
    Projects,
    EvaluationMetrics,
    MetricsInUse
)
from mlfields.utils import metrics_utils


bp = Blueprint('evaluation_metrics', __name__)


@bp.route('', methods=('GET',))
def list(project_id):
    project = Projects.query.filter_by(project_id=project_id).first()
    enabled_metrics_ids = metrics_utils.get_enabled_metrics_ids(project_id)
    metrics = EvaluationMetrics.query
    metric_df = pandas.read_sql(metrics.statement, metrics.session.bind)
    metric_df["In Use"] = False
    metric_df.loc[metric_df["metric_id"].isin(enabled_metrics_ids), "In Use"] = True
    metric_df["url"] = [
        url_for("enable_metrics.disable", project_id=project_id, metric_id=row["metric_id"]) if row["In Use"]\
        else url_for("enable_metrics.enable", project_id=project_id, metric_id=row["metric_id"])
        for i, row in metric_df.iterrows()
    ]
    return render_template(
        'feature_evaluations/list_metrics.html', 
        project=project,  metric_df=metric_df
    )
