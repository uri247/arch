import json
from google.appengine.ext import ndb
from model import Firm, Project, Image, Classification, Client
import main
import web


class ClassificationApi(web.RequestHandler):
    def get(self, firmid):
        self.json_content()
        firm_key = ndb.Key('Firm', firmid)
        query = Classification.query(ancestor=firm_key)
        classifications = query.map(lambda classification: classification.to_dict())
        self.w(json.dumps(classifications))

    def post(self, firmid, clsfid):
        clsf_key = ndb.Key( 'Firm', firmid, 'Classification', clsfid )
        clsf = clsf_key.get()
        if clsf:
            self.error(409)
        else:
            d = json.loads( self.request.body )
            clsf = Classification( key=clsf_key, **d )
            clsf.put()

    def put(self, firmid, clsfid):
        clsf_key = ndb.Key('Firm', firmid, "Classification", clsfid)
        clsf = clsf_key.get()
        if not clsf:
            self.error(404)
        else:
            d = json.loads(self.request.body)
            clsf.populate(**d)
            clsf.put()

    def delete(self, firmid, clsfid):
        clsf_key = ndb.Key("Firm", firmid, "Classification", clsfid)
        clsf = clsf_key.get()
        if not clsf:
            self.error(404)
        else:
            clsf_key.delete()
