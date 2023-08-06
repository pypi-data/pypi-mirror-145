from flask import current_app
from flask_restful import (
    Resource,
    reqparse
)

from mlfields.data_models import (
    db,
    Projects
)


parser = reqparse.RequestParser()
parser.add_argument('name', location=['json', 'args'])
parser.add_argument('note', location=['json', 'args'])


class PJs(Resource):
    def post(self):
        args = parser.parse_args()
        new_project = Projects(name=args['name'], note=args['note'])
        db.session.add(new_project)
        db.session.commit()
        return {"project_id": new_project.project_id}, 201

    def get(self):
        projects = Projects.query
        return [
            {
                "project_id": p.project_id,
                "name": p.name,
                "created": p.created.strftime('%Y-%m-%d %H:%M:%S'),
                "note": p.note
            }
            for p in projects
        ]
