import json
import globals

from google.appengine.ext import blobstore
from google.appengine.ext import ndb
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.api.images import get_serving_url

import model
import web


def create_upload_url(firmid, projid):
    upload_form_url = '/form/image'
    gs_bucket_name = 'frl-arch'
    upload_url = blobstore.create_upload_url(upload_form_url, gs_bucket_name=gs_bucket_name)
    #upload_url = blobstore.create_upload_url(upload_form_url)
    return upload_url


class GetUploadUrlApi(web.RequestHandler):

    def get(self, firmid, projid):
        upload_url = create_upload_url(firmid, projid)
        self.json_content()
        content = json.dumps({'url': upload_url, })
        self.w(content)


class UploadImagesPage(web.RequestHandler):
    def get(self, firmid, projid):
        firm_key = model.firm_key(firmid)
        firm = firm_key.get()
        proj_key = ndb.Key('Firm', firmid, 'Project', projid)
        proj = proj_key.get()

        self.html_content()
        upload_url = create_upload_url(firmid, projid)
        tmpl_name = 'admin/image.html'
        html = globals.jinja_env.get_template(tmpl_name).render({
            'firm': firm.to_dict(),
            'proj': proj,
            'firmid': firmid,
            'projid': projid,
            'upload_url': upload_url,
        })
        self.w(html)


class ImageForm(blobstore_handlers.BlobstoreUploadHandler):
    """A Form handler for uploading images
    """
    def post(self):
        """Post method is the only method"""
        firmid = self.request.get('firmid')
        projid = self.request.get('projid')
        name = self.request.get('name')
        is_front_picture = self.request.get('is_front_picture') == 'yes'

        proj_key = ndb.Key('Firm', firmid, 'Project', projid)
        proj = proj_key.get()

        small_bi = self.get_uploads('small_img')[0]
        large_bi = self.get_uploads('large_img')[0]

        image = model.Image(parent=proj_key, id=name)
        image.name = name
        image.is_front = is_front_picture
        image.small_mime_type = small_bi.content_type
        image.small_blob_key = small_bi.key()
        image.large_mime_type = large_bi.content_type
        image.large_blob_key = large_bi.key()
        image.put()
        if is_front_picture:
            proj.front_picture_id = image.name
            proj.front_picture_url = image.to_dict()['small_url']
            proj.put()
        pass

        self.response.headers['Content-Type'] = 'text/html'
        html = globals.jinja_env.get_template('admin/image_status.html').render({
            'firmid': firmid,
            'projid': projid,
            'imgid': 'short_name',
        })
        self.response.out.write(html)


class ImageResource(web.RequestHandler):
    def get(self, firmid, projid, imgid, size):
        img_key = ndb.Key("Firm", firmid, "Project", projid, "Image", imgid)
        img = img_key.get()
        blob_key = img.large_blob_key if size == 'large' else img.small_blob_key
        url = get_serving_url(blob_key)
        self.redirect(url)


class ImagePage(web.RequestHandler):
    def get(self, firmid, projid, imgid):
        key = model.firm_key(firmid)
        firm = key.get()

        img_key = ndb.Key("Firm", firmid, "Project", projid, "Image", imgid)
        image = img_key.get()
        img = image.to_dict()
        tmpl_name = 'admin/image_data.html'

        self.html_content()
        self.w(globals.jinja_env.get_template(tmpl_name).render({
            'firm': firm.to_dict(),
            'firmid': firmid,
            'projid': projid,
            'imgid': imgid,
            'img': img,
        }))


