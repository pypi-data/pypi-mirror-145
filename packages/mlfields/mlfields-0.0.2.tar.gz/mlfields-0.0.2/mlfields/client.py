import requests


class MLFieldSession(object):
    def __init__(self, host):
        self.session = requests.Session()
        self.url_header = f"http://{host}:5000/api"
        self.project_id = None

    def set_project(self, name, note=""):
        self.project_id = self.get_or_create_project(name, note)

    def get_or_create_project(self, name, note):
        projects = self.session.get(f"{self.url_header}/projects")
        existing_projects = [p for p in projects if p.name == name]
        if existing_projects:
            return existing_projects[0].project_id
        else:
            res = self.session.post(f"{self.url_header}/projects", json=dict(name=name, note=note))
            return res.json()["project_id"]

    def check_project(self):
        def deco(func):
            if not self.project_id:
                raise Exception("Project has not been set")
            return func
        return deco

    @self.check_project
    def register_feature_matrix(self, name, note, df):
        fm_id = self.post_fm(name, note)

    @self.check_project
    def post_fm(self, name, note=""):
        res = self.session.post(
            f"{self.url_header}/projects/{self.project_id}/fms", json=dict(name=name, note=note)
        )
        return res.json()["fm_id"]

    @self.check_project
    def post_fd(self, name, fm_id, note=""):
        pass
