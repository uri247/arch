import dropbox
import os
import re

def get_keys():
    app_key, app_secret = None, None
    keys_fname = os.path.expanduser(os.path.join('~','keys'))
    keys_file = open(keys_fname, 'r')
    rx = re.compile('(\w*)\s*=\s*(\w*)')
    for line in keys_file:
        mobj = rx.match(line)
        if mobj:
            if mobj.group(1) == 'dropbox_arch_app_key': app_key = mobj.group(2)
            if mobj.group(1) == 'dropbox_arch_app_secret' : app_secret = mobj.group(2)
    return app_key, app_secret


def get_client():
    app_key, app_secret = get_keys()
    flow = dropbox.client.DropboxOAuth2FlowNoRedirect(app_key, app_secret)
    auth_url = flow.start()
    print '1. Go to: ' + auth_url
    print '2. Click "Allow"'
    print '3. Copy the authorization code.'
    code = raw_input('Enter the authorization code here: ').strip()
    access_token, user_id = flow.finish(code)
    client = dropbox.client.DropboxClient(access_token)
    return client

def main():
    client = get_client()
    print 'linked account: ', client.account_info()
    result = client.share('hi.txt')
    print result
    result2 = client.media('hi.txt')
    print result2
    result3 = client.media(r'Frl-Arch/WebRes/Herzelia_Sokolov/180x124/15F-Sokolov_180x124.jpg')
    print result3

if __name__ == '__main__':
    main()