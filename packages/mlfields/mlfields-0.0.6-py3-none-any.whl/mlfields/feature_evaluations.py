from flask import (
    Blueprint,
    render_template,
    url_for
)
import pandas

from mlfields.data_models import (
    Projects,
    FeatureMatrices,
    FeatureDefinitions,
    FeatureEvaluations
)
from mlfields.utils import metrics_utils


bp = Blueprint('feature_evaluations', __name__)


@bp.route('', methods=('GET',))
def list(project_id, fm_id):
    project = Projects.query.filter_by(project_id=project_id).first()
    fm = FeatureMatrices.query.filter_by(fm_id=fm_id).first()
    fes = FeatureEvaluations.query.filter_by(fm_id=fm_id)
    fds = FeatureDefinitions.query.filter_by(project_id=project_id)
    df = pandas.read_sql(fes.statement, fes.session.bind)
    fds_df = pandas.read_sql(fds.statement, fds.session.bind)[["feature_id", "name"]]
    metric_name_df = metrics_utils.get_enabled_metrics_df(project_id)
    eval_df = df.merge(metric_name_df, on="metric_id", how="left")
    eval_df = eval_df[~eval_df["metric_name"].isnull()]
    eval_df = eval_df.pivot(index=["feature_id"], columns="metric_name", values="value").reset_index()
    eval_df["feature_id"] = eval_df["feature_id"].astype('int64')
    eval_df = eval_df.merge(fds_df, on="feature_id", how="left")
    return render_template(
        'feature_evaluations/list.html', 
        project=project, fm=fm, metrics=metric_name_df["metric_name"].values, eval_df=eval_df
    )
