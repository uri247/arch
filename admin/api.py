import json
from google.appengine.ext import ndb
from model import Firm, Project, Image, Classification, Client
from google.appengine.ext import deferred
from google.appengine.api import mail
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


class ProcessApi(web.RequestHandler):
    def get(self, firmid, process):
        self.json_content()
        firm_key = ndb.Key('Firm', firmid)

        if process == 'hierarchy':

            def do_hier():
                projects = dict()
                for proj in Project.query(ancestor=firm_key):
                    projects[proj.key.id()] = proj.to_dict()
                    projects[proj.key.id()]['images'] = []

                for img in Image.query(ancestor=firm_key).order(Image.key):
                    img_d = img.to_dict( exclude=['small_blob_key', 'large_blob_key'] )
                    projects[img.key.parent().id()]['images'].append( img_d )

                mail.send_mail( sender = 'Uri London <uri@finrav.co.il>', to = 'uri.london@live.com',
                                subject = 'deferred defer', body = json.dumps(projects))

            deferred.defer( do_hier )

            self.w( json.dumps("ok") )

        elif process == 'mail':
            mail.send_mail( sender = 'Uri London <uri@finrav.co.il>',
                            to = 'Live Person <uri.london@live.com>',
                            subject = 'your test has succeeded',
                            body = 'Dear Live Person,\n\n    I\'m happy to tell you that your test is good'
                            )
            self.w( json.dumps('ok') )

