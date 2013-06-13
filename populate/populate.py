import json
import sys
import os
import requests

import data

#base_url is either local or remote:
if len(sys.argv) == 1 or sys.argv[1] == 'local':
    base_url = 'http://localhost:8080'
elif sys.argv[1] == 'remote':
    base_url = 'http://www.frl-arch.com'
else:
    print 'sys.argv[0] [local|remote]'
    exit()
    
image_dir= os.path.join( os.path.dirname(__file__), 'images' )

#URL methods
def firm_url(firmid):
    return '%s/api/firm/%s' % (base_url, firmid)
def project_url(firmid,projid):
    return '%s/api/project/%s/%s' % (base_url, firmid, projid) 
def image_url(firmid,projid,imageid):
    return '%s/admin/image_form' % (base_url,)

def delete_firm():
    requests.delete( firm_url(data.firmid) )

def popuplate_firm():
    r = requests.post( firm_url(data.firmid), json.dumps(data.firm_data) )
    print 'status %d setting firm' % r.status_code
        
def populate_projects():
    for projid in data.projects_data:
        p = data.projects_data[projid]
        r = requests.post( project_url(data.firmid, projid), json.dumps(p['data']) )
        print 'status %d setting project %s' % (r.status_code, projid)
        populate_images(p)
    
def populate_images(proj):
    for img_name in proj['images']:
        imgid = img_name[:img_name.find(os.path.extsep)]
        r = requests.post( 
            image_url(data.firmid, proj['id'], imgid),
            data = {
                'firmid': data.firmid,
                'projid': proj['id'],
                'name': imgid,
            },
            files = {
                'file': open( os.path.join(image_dir,img_name), 'rb' )
        })
        print 'status %d sending image %s' % (r.status_code, img_name)
        pass
    pass

def main():
    delete_firm()
    popuplate_firm()
    populate_projects()


if __name__ == '__main__':
    main()
