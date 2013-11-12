import json
from google.appengine.ext import ndb
from google.appengine.ext import deferred
from google.appengine.api import mail, files

from model import Firm, Project, Image, Classification, Client
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


def process_hier():
    firmid = 'frl'
    firm_key = ndb.Key('Firm', firmid)
    projects = dict()
    for proj in Project.query(ancestor=firm_key):
        projects[proj.key.id()] = proj.to_dict()
        projects[proj.key.id()]['images'] = []

    for img in Image.query(ancestor=firm_key).order(Image.key):
        img_d = img.to_dict( exclude=['small_blob_key', 'large_blob_key'] )
        projects[img.key.parent().id()]['images'].append( img_d )

    fname = '/gs/frl-arch/' + firmid + '/json/proj-detailed.json'
    wfname = files.gs.create( fname, mime_type='application/javascript', acl='public-read')
    with files.open(wfname, 'a') as f:
        f.write( json.dumps(projects) )
    files.finalize(wfname)


class ProcessApi(web.RequestHandler):
    def get(self, firmid, process):
        self.json_content()
        firm_key = ndb.Key('Firm', firmid)

        if process == 'process_hier':
            deferred.defer( process_hier )
            self.w( json.dumps("ok") )

        if process == 'get_hier':
            fname = '/gs/frl-arch/' + firmid + '/json/proj-detailed.json'
            with files.open(fname, 'r') as f:
                data = f.read(60 * 1000)
                while data:
                    self.w( data )
                    data = f.read(60 * 1000)

        elif process == 'mail':
            mail.send_mail( sender = 'Uri London <uri@finrav.co.il>',
                            to = 'Live Person <uri.london@live.com>',
                            subject = 'your test has succeeded',
                            body = 'Dear Live Person,\n\n    I\'m happy to tell you that your test is good'
                            )
            self.w( json.dumps('ok') )

        elif process == 'test_file':
            fname = '/gs/frl-arch/test.html'
            wfname = files.gs.create( fname, mime_type='text/html', acl='public-read')
            with files.open(wfname, 'a') as f:
                f.write( 'hello world' )
                f.write( 'bye bye' )
            files.finalize(wfname)

    pass

