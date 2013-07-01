import json

from google.appengine.ext import blobstore
from google.appengine.ext import ndb
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.api.images import get_serving_url

import model
import main
import web


def create_upload_url(firmid, projid):
    upload_form_url = '/form/image'
    gs_bucket_name = 'frl-arch'
    upload_url = blobstore.create_upload_url(upload_form_url, gs_bucket_name=gs_bucket_name)
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
        html = main.jinja_env.get_template(tmpl_name).render({
            'firm': firm.to_dict(),
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
        proj_key = ndb.Key('Firm', firmid, 'Project', projid)

        files = self.get_uploads('file')
        for blob_info in files:
            image = model.Image(parent=proj_key, id=blob_info.filename)
            image.name = self.request.get('name')
            image.mime_type = blob_info.content_type
            image.blob_key = blob_info.key()
            image.put()
            pass

        self.response.headers['Content-Type'] = 'text/html'
        html = main.jinja_env.get_template('admin/image_status.html').render({
            'firmid': firmid,
            'projid': projid,
            'imgid': 'short_name',
        })
        self.response.out.write(html)


class ImageResource(web.RequestHandler):
    def get(self, firmid, projid, imgid):
        img_key = ndb.Key("Firm", firmid, "Project", projid, "Image", imgid)
        img = img_key.get()
        url = get_serving_url(img.blob_key)
        self.redirect(url)


class ImagePage(web.RequestHandler):
    def get(self, firmid, projid, imgid):
        key = model.firm_key(firmid)
        firm = key.get()

        img = {}
        tmpl_name = None;

        img_key = ndb.Key("Firm", firmid, "Project", projid, "Image", imgid)
        image = img_key.get()
        img = image.to_dict()
        tmpl_name = 'admin/image_data.html'

        self.html_content()
        self.w(main.jinja_env.get_template(tmpl_name).render({
            'firm': firm.to_dict(),
            'firmid': firmid,
            'projid': projid,
            'imgid': imgid,
            'img': img,
        }))


