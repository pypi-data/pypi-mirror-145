from mlfields.data_models import (
    db,
    FeatureEvaluations
)
from flask_restful import (
    Resource,
    reqparse
)


parser = reqparse.RequestParser()
parser.add_argument('feature_id')
parser.add_argument('metric_id')
parser.add_argument('value')


class FEs(Resource):
    def post(self, project_id, fm_id):
        args = parser.parse_args()
        new_fe = FeatureEvaluations(
            fm_id=fm_id,
            feature_id=args["feature_id"],
            metric_id=args["metric_id"],
            value=args["value"]
        )
        db.session.add(new_fe)
        db.session.commit()
        return {}, 201

    def get(self, project_id, fm_id):
        fes = FeatureEvaluations.query.filter_by(project_id=project_id, fm_id=fm_id)
        return [
            dict(
                fm_id=fe.fm_id,
                feature_id=fe.feature_id,
                metric_id=fe.metric_id,
                value=fe.value
            )
            for fe in fes
        ]
