import requests
import json
import test_literals as data


base_url = 'http://localhost:8080/api'
def firm_url(firmid):
    return '%s/firm/%s' % (base_url, firmid)
def project_url(firmid,projid):
    return '%s/project/%s/%s' % (base_url, firmid, projid) 

def delete_firm():
    requests.delete( firm_url(data.firmid) )

def popuplate_firm():
    r = requests.post( firm_url(data.firmid), json.dumps(data.firm_data) )
    print 'status %d setting firm' % r.status_code
    
def populate_projects():
    for projid in data.projects_data:
        p = data.projects_data[projid]
        r = requests.post( project_url(data.firmid, projid), json.dumps(p) )
        print 'status %d setting project %s' % (r.status_code, projid)
    
def main():
    delete_firm()
    popuplate_firm()
    populate_projects()


if __name__ == '__main__':
    main()
