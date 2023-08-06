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


bp = Blueprint('feature_evaluations_for_each_feature', __name__)


@bp.route('', methods=('GET',))
def list(project_id, feature_id):
    project = Projects.query.filter_by(project_id=project_id).first()
    fes = FeatureEvaluations.query.filter_by(feature_id=feature_id)
    fms = FeatureMatrices.query
    fd = FeatureDefinitions.query.filter_by(feature_id=feature_id).first()
    df = pandas.read_sql(fes.statement, fes.session.bind)
    metric_name_df = metrics_utils.get_enabled_metrics_df(project_id)
    fms_df = pandas.read_sql(fms.statement, fms.session.bind)[["fm_id", "name", "created"]]
    eval_df = df.merge(metric_name_df, on="metric_id", how="left")
    eval_df = eval_df[~eval_df["metric_name"].isnull()]
    eval_df = eval_df.pivot(index=["fm_id"], columns="metric_name", values="value").reset_index()
    eval_df["fm_id"] = eval_df["fm_id"].astype('int64')
    eval_df = eval_df.merge(fms_df, on="fm_id", how="left")
    return render_template(
        'feature_evaluations/list_for_each_feature.html', 
        project=project, fd=fd, metrics=metric_name_df["metric_name"].values, eval_df=eval_df
    )

