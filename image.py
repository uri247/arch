#from google.appengine.ext import blobstore
from google.appengine.ext import ndb
import model
import main
import web


class ImagePage(web.RequestHandler):
    def get(self, firmid, projid):
        #projid = self.request.get('projid')
        #upload_url = blobstore.create_upload_url('')
        self.html_content()
        self.w( main.jinja_env.get_template( 'image.html' ).render({
            'firmid': firmid,
            'projid': projid,                                          
            }))


class ImageForm(web.RequestHandler):
    def post(self):
        firmid = self.request.get('firmid')
        projid = self.request.get('projid')
        
        short_name = self.request.get('name')
        f = self.request.POST['file']
        
        image_key = ndb.Key( "Firm", firmid, "Proj", projid, "Image", short_name )
        image = model.Image( key = image_key )
        image.short_name = short_name
        image.orig_name = f.filename
        image.mime_type = f.type
        image.data = self.request.get('file')
        image.put()
               
        self.html_content()
        self.w( 'A new image for firm %s, project %s success<br>' % (firmid, projid) )
        self.w( 'short name: %s' % (short_name,) )
        self.w( 'OK' )
        
        
class ImageResource(web.RequestHandler):
    def get(self, firmid, projid, imgid):
        img_key = ndb.Key( "Firm", firmid, "Proj", projid, "Image", imgid )
        img = img_key.get()
        self.response.headers['Content-Type'] = str(img.mime_type)
        self.w( img.data )
        
