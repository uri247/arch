import json
from google.appengine.ext import ndb
from model import Firm, Project, Image

def hierarchy():
    firm_key = ndb.Key('Firm', 'frl')
    projects = dict()
    for proj in Project.query(ancestor=firm_key):
        print proj.key.id()
        projects[proj.key.id()] = proj.to_dict()
        projects[proj.key.id()]['images'] = []

    for img in Image.query(ancestor=firm_key).order(Image.key):
        print img.key.id()
        img_d = img.to_dict( exclude=['small_blob_key', 'large_blob_key'] )
        projects[img.key.parent().id()]['images'].append( img_d )

    print json.dumps(projects)


