from mlfields.data_models import (
    db,
    FeatureDefinitions
)
from flask_restful import (
    Resource,
    reqparse
)


parser = reqparse.RequestParser()
parser.add_argument('name')
parser.add_argument('note')


class FDs(Resource):
    def post(self, project_id):
        args = parser.parse_args()
        new_fd = FeatureDefinitions(
            project_id=project_id,
            name=args["name"],
            note=args["note"]
        )
        db.session.add(new_fd)
        db.session.commit()
        return {"feature_id": new_fd.feature_id}, 201

    def get(self, project_id):
        fds = FeatureDefinitions.query.filter_by(project_id=project_id)
        return [
            dict(
                feature_id=fd.feature_id,
                name=fd.name,
                note=fd.note
            )
            for fd in fds
        ]
