import json
import sys
import os
import requests

from data import firmid, firm_data
from xldata import read_xl, small_folder, large_folder, small_suffix, large_suffix, xl_file, image_dir

#base_url is either local or remote:
if len(sys.argv) == 1 or sys.argv[1] == 'local':
    base_url = 'http://localhost:8080'
elif sys.argv[1] == 'remote':
    base_url = 'http://www.frl-arch.com'
else:
    print 'sys.argv[0] [local|remote]'
    exit()
    

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
                'firmid': firmid,
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
    delete_firm()
    populate_firm()
    populate_projects()


if __name__ == '__main__':
    main()
