import json
import sys
import os
from unittest.test.test_result import __init__
import requests

from xldata import XlData


small_folder = '180x124'
large_folder = '738x514'
small_suffix = '_180x124'
large_suffix = '_738x514'
xl_file = os.path.join( os.path.expanduser('~'), 'dropbox', 'frl-arch', 'summary.xlsx' )
image_dir = os.path.join( os.path.expanduser('~'), 'dropbox', 'frl-arch', 'webres' )

proxies = None
xldata = None
urls = None

class Urls(object):
    def __init__(self):
        if len(sys.argv) == 1 or sys.argv[1] == 'local':
            self.base_url = 'http://localhost:8080'
        elif sys.argv[1] == 'remote':
            self.base_url = 'http://www.frl-arch.com'
        else:
            print 'sys.argv[0] [local|remote]'
            exit()

    def firm_url(self, firmid):
        return '%s/api/firm/%s' % (self.base_url, firmid)

    def project_url(self, firmid, projid):
        return '%s/api/project/%s/%s' % (self.base_url, firmid, projid)

    def clsf_url(self, firmid, clsfid ):
        return '%s/api/classification/%s/%s' % (self.base_url, firmid, clsfid)

    def getupurl_url(self, firmid, projid):
        return '%s/api/get-upload-url/%s/%s' % (self.base_url, firmid, projid)


def delete_firm():
    requests.delete( urls.firm_url(xldata.firm['id']), proxies = proxies )

def populate_firm():
    r = requests.post( urls.firm_url(xldata.firm['id']), json.dumps(xldata.firm['data']), proxies = proxies )
    print 'status %d setting firm' % r.status_code

def populate_classifications():
    for clsfid, clsf in xldata.classifications.iteritems():
        r = requests.post( urls.clsf_url(xldata.firm['id'], clsfid), json.dumps(clsf['data']), proxies=proxies )
        print 'status %d setting classification %s' % (r.status_code, clsfid)

def populate_projects():
    for projid, proj in xldata.projects.iteritems():
        r = requests.post( urls.project_url(xldata.firm['id'], projid), json.dumps(proj['data']), proxies=proxies )
        print 'status %d setting project %s' % (r.status_code, projid)
        if r.status_code == 200:
            populate_images(proj)
    
def populate_images(proj):
    for img_name in proj['images']:
        r = requests.get( urls.getupurl_url(xldata.firm['id'], proj['id']), proxies=proxies )
        upurl = r.json()['url']
        small_img_name = os.path.join( image_dir, proj['id'], small_folder, img_name + small_suffix + '.jpg' )
        large_img_name = os.path.join( image_dir, proj['id'], large_folder, img_name + large_suffix + '.jpg' )
        is_front_picture = 'yes' if proj['data']['front_picture_id'] == img_name else 'no'

        small_img, large_img = None, None
        try:
            small_img = open( small_img_name, 'rb')
            large_img = open( large_img_name, 'rb')
        except IOError as e:
            print 'error opening %s' % (e.filename,)
            print e.message
            continue

        r = requests.post( 
            upurl,
            data={
                'firmid': xldata.firm['id'],
                'projid': proj['id'],
                'name': img_name,
                'is_front_picture': is_front_picture,
            },
            files = {
                'small_img': open( small_img_name, 'rb' ),
                'large_img': open( large_img_name, 'rb' )
            },
            proxies = proxies
        )
        print 'status %d sending image %s' % (r.status_code, img_name)
        pass
    pass

def main():
    global xldata, urls

    xldata = XlData(xl_file, small_folder, large_folder, small_suffix, large_suffix)
    xldata.read()
    urls = Urls()

    delete_firm()
    populate_firm()
    populate_classifications()
    populate_projects()


if __name__ == '__main__':
    main()
