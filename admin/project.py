import json
from google.appengine.ext import ndb
import model
import main
import web


class ProjectPage(web.RequestHandler):
    def get(self, firmid, projid):
        """

        :param firmid:
        :param projid:
        """
        new_proj = None
        p = None
        images = None
        firm_key = model.firm_key(firmid)
        firm = firm_key.get()

        if projid:
            new_proj = False
            key = ndb.Key("Firm", firmid, "Project", projid)
            p = key.get().to_dict()
            _images = model.Image.query(ancestor=key).fetch()
            images = [img.to_dict() for img in _images]

        else:
            new_proj = True
            p = {}
            images = []

        tmpl = main.jinja_env.get_template('admin/project.html')
        html = tmpl.render({
            'firmid': firmid,
            'projid': projid,
            'firm': firm.to_dict(),
            'new_proj': new_proj,
            'p': p,
            'images': images,
        })
        self.html_content()
        self.w(html)
        pass


class ProjectForm(web.RequestHandler):
    def post(self):
        firmid = self.request.get('firmid')
        projid = self.request.get('projid')
        new_proj = self.request.get('new_proj')
        proj = None
        key = ndb.Key('Firm', firmid, 'Project', projid)

        if new_proj:
            proj = model.Project(key=key)
        else:
            proj = key.get()

        proj.populate(
            title_e=self.request.get('title_e'),
            title_h=self.request.get('title_h'),
            address_e=self.request.get('address_e'),
            address_h=self.request.get('address_h'),
            year=int(self.request.get('year')),
            description_e=self.request.get('description_e'),
            description_h=self.request.get('description_h'),
            status=self.request.get('status'),
            plot_area=int(self.request.get('plot_area')),
            built_area=int(self.request.get('built_area')),
            classification=self.request.get('classification')
        )
        proj.put()
        self.redirect('/%s/admin/firm' % firmid)


class ProjectApi(web.RequestHandler):
    def get(self, firmid, projid):
        """return a list of projects for a firm, or project detail
        """
        self.json_content()
        if not projid:
            #user wants all projects
            firm_key = ndb.Key("Firm", firmid)
            _projects = model.Project.query_firm(firm_key)
            projects = [p.to_dict() for p in _projects]
            self.w(json.dumps(projects))
        else:
            #we return a specific project
            proj_key = ndb.Key("Firm", firmid, "Project", projid)
            proj = proj_key.get()
            d = proj.to_dict()
            self.w(json.dumps(d))

    def post(self, firmid, projid):
        """create a new project with a given projid
        """
        proj_key = ndb.Key("Firm", firmid, "Project", projid)
        proj = proj_key.get()
        if proj:
            self.error(409)
        else:
            d = json.loads(self.request.body)
            proj = model.Project(key=proj_key, **d)
            proj.put()

    def put(self, firmid, projid):
        proj_key = ndb.Key("Firm", firmid, "Project", projid)
        proj = proj_key.get()
        if not proj:
            self.error(404)
        else:
            d = json.loads(self.request.body)
            proj.populate(**d)
            proj.put()

    def delete(self, firmid, projid):
        proj_key = ndb.Key("Firm", firmid, "Project", projid)
        proj = proj_key.get()
        if not proj:
            self.error(404)
        else:
            proj_key.delete()
