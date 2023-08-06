from mlfields.data_models import EvaluationMetrics


def insert_all(db):
    metrics = [
        EvaluationMetrics(
            metric_name="min",
            script="""\
def get_metric_func():
    import numpy
    def func(feature_vec, target_vec):
        return numpy.min(feature_vec)
    return func
"""
        ),
        EvaluationMetrics(
            metric_name="max",
            script="""\
def get_metric_func():
    import numpy
    def func(feature_vec, target_vec):
        return numpy.max(feature_vec)
    return func
"""
        ),
        EvaluationMetrics(
            metric_name="mean",
            script="""\
def get_metric_func():
    import numpy
    def func(feature_vec, target_vec):
        return numpy.mean(feature_vec)
    return func
"""
        ),
        EvaluationMetrics(
            metric_name="std",
            script="""\
def get_metric_func():
    import numpy
    def func(feature_vec, target_vec):
        return numpy.std(feature_vec)
    return func
"""
        ),
        EvaluationMetrics(
            metric_name="correlation",
            script="""\
def get_metric_func():
    from scipy.stats import pearsonr
    def func(feature_vec, target_vec):
        corr, _ = pearsonr(feature_vec, target_vec)
        return corr
    return func
"""
        ),
        EvaluationMetrics(
            metric_name="MI (rg)",
            script="""\
def get_metric_func():
    from sklearn.feature_selection import mutual_info_regression
    def func(feature_vec, target_vec):
        mi = mutual_info_regression(feature_vec.reshape(-1, 1), target_vec)
        return mi[0]
    return func
"""
        ),
        EvaluationMetrics(
            metric_name="MI (cl)",
            script="""\
def get_metric_func():
    from sklearn.feature_selection import mutual_info_classif
    def func(feature_vec, target_vec):
        mi = mutual_info_classif(feature_vec.reshape(-1, 1), target_vec)
        return mi[0]
    return func
"""
        )
    ]
    for m in metrics:
        db.session.add(m)
        db.session.commit()
