from mlfields.data_models import (
    db,
    FeatureMatrices
)
from flask_restful import (
    Resource,
    reqparse
)


parser = reqparse.RequestParser()
parser.add_argument('name')
parser.add_argument('note')


class FMs(Resource):
    def post(self, project_id):
        args = parser.parse_args()
        new_fm = FeatureMatrices(
            project_id=project_id,
            name=args["name"],
            note=args["note"]
        )
        db.session.add(new_fm)
        db.session.commit()
        return {"fm_id": new_fm.fm_id}, 201
