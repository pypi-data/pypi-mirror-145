from mlfields.data_models import (
    db,
    MetricsInUse
)
from flask_restful import (
    Resource,
    reqparse
)


parser = reqparse.RequestParser()
parser.add_argument('metric_id')


class MIUs(Resource):
    def put(self, project_id):
        args = parser.parse_args()
        new_fm = MetricsInUse(
            project_id=project_id,
            metric_id=args["metric_id"]
        )
        db.session.add(new_fm)
        db.session.commit()
        return {"fm_id": new_fm.fm_id}, 201

    def get(self, project_id):
        mius = MetricsInUse.query.filter_by(project_id=project_id)
        return [
            miu.metric_id
            for miu in mius 
        ]

    def delete(self, project_id):
        args = parser.parse_args()
        mius = MetricsInUse.query.filter_by(project_id=project_id, metric_id=args["metric_id"])
        db.session.delete(mius)
        db.session.commit()
        return {}, 204
