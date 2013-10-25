import json
import sys
import os
import requests

from data import firmid, firm_data
from xldata import read_xl

#base_url is either local or remote:
if len(sys.argv) == 1 or sys.argv[1] == 'local':
    base_url = 'http://localhost:8080'
elif sys.argv[1] == 'remote':
    base_url = 'http://www.frl-arch.com'
else:
    print 'sys.argv[0] [local|remote]'
    exit()
    


xl_file = os.path.join( os.path.expanduser('~'), 'dropbox', 'frl-arch', 'summary.xlsx' )
image_dir = os.path.join( os.path.expanduser('~'), 'dropbox', 'frl-arch', 'webres' )
projects_data = read_xl(xl_file)
proxies = None

#URL methods
def firm_url(firmid):
    return '%s/api/firm/%s' % (base_url, firmid)

def project_url(firmid,projid):
    return '%s/api/project/%s/%s' % (base_url, firmid, projid) 

def getupurl_url(firmid,projid):
    return '%s/api/get-upload-url/%s/%s' % (base_url, firmid, projid)


def delete_firm():
    requests.delete( firm_url(firmid), proxies = proxies )

def populate_firm():
    r = requests.post( firm_url(firmid), json.dumps(firm_data), proxies = proxies )
    print 'status %d setting firm' % r.status_code
        
def populate_projects():
    for projid in projects_data:
        p = projects_data[projid]
        r = requests.post( project_url(firmid, projid), json.dumps(p['data']), proxies=proxies )
        print 'status %d setting project %s' % (r.status_code, projid)
        populate_images(p)
    
def populate_images(proj):
    for img_name in proj['images']:
        r = requests.get( getupurl_url(firmid, proj['id']), proxies=proxies )
        upurl = r.json()['url']
        name = img_name[:img_name.find('.')]
        is_front_picture = 'yes' if proj['data']['front_picture_id'] == img_name else 'no'

        r = requests.post( 
            upurl,
            data={
                'firmid': firmid,
                'projid': proj['id'],
                'name': name,
                'is_front_picture': is_front_picture,
            },
            files = {
                'file': open( os.path.join(image_dir, proj['id'], '180x124', img_name), 'rb' )
            },
            proxies = proxies
        )
        print 'status %d sending image %s' % (r.status_code, img_name)
        pass
    pass

def main():
    delete_firm()
    populate_firm()
    populate_projects()


if __name__ == '__main__':
    main()
