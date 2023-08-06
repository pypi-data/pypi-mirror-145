from flask import (
    Blueprint,
    url_for,
    redirect
)
import pandas

from mlfields.data_models import (
    db,
    MetricsInUse
)
from mlfields.utils import metrics_utils


bp = Blueprint('enable_metrics', __name__)


@bp.route('enable/', methods=('GET',))
def enable(project_id, metric_id):
    new_miu = MetricsInUse(project_id=project_id, metric_id=metric_id)
    db.session.add(new_miu)
    db.session.commit()
    return redirect(url_for('evaluation_metrics.list', project_id=project_id))


@bp.route('disable/', methods=('GET',))
def disable(project_id, metric_id):
    miu = MetricsInUse.query.filter_by(project_id=project_id, metric_id=metric_id).first()
    db.session.delete(miu)
    db.session.commit()
    return redirect(url_for('evaluation_metrics.list', project_id=project_id))
