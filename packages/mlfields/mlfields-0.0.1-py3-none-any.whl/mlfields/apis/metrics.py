from mlfields.data_models import (
    db,
    EvaluationMetrics
)
from flask_restful import (
    Resource,
    reqparse
)


parser = reqparse.RequestParser()
parser.add_argument('name')


class Metrics(Resource):
    def post(self, project_id):
        args = parser.parse_args()
        new_metric = EvaluationMetrics(
            project_id=project_id,
            metric_name=args["name"]
        )
        db.session.add(new_metric)
        db.session.commit()
        return {"metric_id": new_metric.metric_id}, 201

    def get(self, project_id):
        metrics = EvaluationMetrics.query.filter_by(project_id=project_id)
        return [
            dict(
                metric.metric_id,
                metric.metric_name
            )
            for metric in metrics
        ]
