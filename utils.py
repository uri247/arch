import json
from google.appengine.ext import ndb
from google.appengine.ext.blobstore import BlobInfo
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



def all_entities():
    k = ndb.Key('Firm', 'frl')
    #return the iterator
    return ndb.Query(ancestor=k).iter(keys_only=True)

def print_all_entities():
    for x in all_entities():
        print x


def delete_all_images():
    k = ndb.Key('Firm', 'frl')
    for img in Image.query(ancestor=k).iter():
        print img.key.id()
	for bk in [img.small_blob_key, img.large_blob_key]:
            if BlobInfo.get(bk):
                BlobInfo.get(bk).delete()
        img.key.delete()

