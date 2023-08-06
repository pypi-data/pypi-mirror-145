import requests
import numpy


class MLFieldSession(object):
    def __init__(self, host):
        self.session = requests.Session()
        self.url_header = f"http://{host}:5000/api"
        self.project_id = None

    def set_project(self, name, note=""):
        self.project_id = self.get_or_create_project(name, note)

    def get_or_create_project(self, name, note):
        projects = self.session.get(f"{self.url_header}/projects/").json()
        existing_projects = [p for p in projects if p["name"] == name]
        if existing_projects:
            return existing_projects[0]["project_id"]
        else:
            res = self.session.post(f"{self.url_header}/projects/", json=dict(name=name, note=note))
            return res.json()["project_id"]

    def _check_project(func):
        def deco(self, *args, **kwargs):
            if not self.project_id:
                raise Exception("Project has not been set")
            return func(self, *args, **kwargs)
        return deco
    
    @_check_project
    def register_metric(self, name, script):
        self._test_func(script)
        res = self.session.post(
            f"{self.url_header}/projects/{self.project_id}/metrics/", json=dict(name=name, script=script)
        )
        return res.json()["metric_id"]
    
    @_check_project
    def get_metric_func(self):
        res = self.session.get(
            f"{self.url_header}/projects/{self.project_id}/metrics/"
        )
        return {
            m["metric_id"]: self._get_func(m["script"])
            for m in res.json()
        }

    @_check_project
    def register_feature_matrix(self, df, target_column, name, note="", feature_columns=[], feature_names_dict={}):
        feature_columns = feature_columns or [c for c in df.columns if c != target_column]
        feature_ids = self._get_or_create_feature_ids(df[feature_columns], feature_names_dict)
        fm_id = self.get_or_create_fm(name, note)
        metric_func = self.get_metric_func()
        for cname, fid in feature_ids.items():
            for mid, mfunc in metric_func.items():
                v = mfunc(df[cname].values, df[target_column].values)
                self.post_evaluation(fm_id, fid, mid, v)
                
    @_check_project
    def get_or_create_fm(self, name, note):
        fms = self.session.get(f"{self.url_header}/projects/{self.project_id}/fms/").json()
        existing_fms = [fm for fm in fms if fm["name"]==name]
        if existing_fms:
            return existing_fms[0]["fm_id"]
        else:
            return self.post_fm(name, note)
        

    @_check_project
    def post_fm(self, name, note):
        res = self.session.post(
            f"{self.url_header}/projects/{self.project_id}/fms/", json=dict(name=name, note=note)
        )
        return res.json()["fm_id"]

    @_check_project
    def post_fd(self, name, note=""):
        res = self.session.post(
            f"{self.url_header}/projects/{self.project_id}/fds/", json=dict(name=name, note=note)
        )
        return res.json()["feature_id"]
    
    @_check_project
    def post_evaluation(self, fm_id, feature_id, metric_id, value):
        res = self.session.post(
            f"{self.url_header}/projects/{self.project_id}/fms/{fm_id}/", 
            json=dict(metric_id=metric_id, feature_id=feature_id, value=value)
        )

    @_check_project
    def _get_or_create_feature_ids(self, df, feature_names_dict={}):
        fds = self.session.get(f"{self.url_header}/projects/{self.project_id}/fds/").json()
        feature_id_dict = {
            fd["name"]: fd["feature_id"]
            for fd in fds
        }
        ret_dict = {}
        for c in df.columns:
            name = feature_names_dict.get(c) or c
            feature_id = feature_id_dict.get(name) or self.post_fd(name)
            ret_dict[name] = feature_id
        return ret_dict
    
    def _test_func(self, string):
        func = self._get_func(string)
        vec1 = numpy.array([1, 2, 3, 4, 5])
        vec2 = numpy.array([0, 1, 0, 1, 1])
        try:
            func(vec1, vec2)
        except e:
            raise(e)
    
    @staticmethod
    def _get_func(string):
        exec(string, globals())
        return get_metric_func()
