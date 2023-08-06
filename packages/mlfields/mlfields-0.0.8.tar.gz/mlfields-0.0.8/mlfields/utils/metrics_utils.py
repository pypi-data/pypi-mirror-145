import pandas

from mlfields.data_models import (
    EvaluationMetrics,
    MetricsInUse
)


def get_enabled_metrics_ids(project_id):
    enabled_metrics = MetricsInUse.query.filter_by(project_id=project_id)
    return [m.metric_id for m in enabled_metrics]


def get_enabled_metrics_df(project_id):
    enabled_metrics_ids = get_enabled_metrics_ids(project_id)
    metrics = EvaluationMetrics.query
    metric_name_df = pandas.read_sql(metrics.statement, metrics.session.bind)[["metric_id", "metric_name"]].sort_values(by="metric_id")
    return metric_name_df[metric_name_df["metric_id"].isin(enabled_metrics_ids)].sort_values(by="metric_id")
