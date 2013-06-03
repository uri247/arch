from google.appengine.ext import blobstore


class ImagePage(web.RequestHandler):
    def get(self, firm, projid):
        #projid = self.request.get('projid')
        new_proj = None
        proj = None
        
        if( projid ):
            new_proj = False
            key = ndb.Key( "Firm", self.get_firmid(), "Project", projid )
            proj = key.get()
        else:
            new_proj = True
            proj = model.Project()
            



    def get(self):
        up_url = blobstore.create_upload_url('/fallrec/upload')
        template = jinja_environment.get_template('fallrec.html')
        context = {
            'up_url': up_url,
            'title': 'Fall Rectangle',
        }
        self.w( template.render(context))

