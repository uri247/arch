#from google.appengine.ext import blobstore
from google.appengine.ext import ndb
import model
import main
import web


class ImagePage(web.RequestHandler):
    def get(self, firmid, projid, imgid):
        img = {}
        tmpl_name = None;

        if imgid:
            img_key = ndb.Key( "Firm", firmid, "Project", projid, "Image", imgid )
            image = img_key.get()
            img = image.to_dict()
            tmpl_name = 'admin/image_data.html'
        else:
            tmpl_name = 'admin/image.html'
         
            
        self.html_content()
        self.w( main.jinja_env.get_template( tmpl_name ).render({
            'firmid': firmid,
            'projid': projid,
            'imgid': imgid,
            'img': img,
        }))



class ImageForm(web.RequestHandler):
    def post(self):
        firmid = self.request.get('firmid')
        projid = self.request.get('projid')
        
        short_name = self.request.get('name')
        f = self.request.POST['file']
        
        image_key = ndb.Key( "Firm", firmid, "Project", projid, "Image", short_name )
        image = model.Image( key = image_key )
        image.short_name = short_name
        image.orig_name = f.filename
        image.mime_type = f.type
        image.data = self.request.get('file')
        image.put()
               
        self.html_content()
        self.w( main.jinja_env.get_template( 'admin/image_status.html' ).render({
            'firmid': firmid,
            'projid': projid,
            'imgid': short_name,
        }))        
        
class ImageResource(web.RequestHandler):
    def get(self, firmid, projid, imgid):
        img_key = ndb.Key( "Firm", firmid, "Project", projid, "Image", imgid )
        img = img_key.get()
        self.response.headers['Content-Type'] = str(img.mime_type)
        self.w( img.data )
        
