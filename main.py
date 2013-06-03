import jinja2
import os
from google.appengine.ext import webapp
import firm
import project
import image

static_dir =  os.path.join( os.path.dirname(__file__), 'static' )
jinja_env = jinja2.Environment( loader=jinja2.FileSystemLoader( static_dir ) )


class MainPage(webapp.RequestHandler):
    def get(self):
        self.redirect( '/admin/firm' )
        


application = webapp.WSGIApplication([
        ('/', MainPage),
        ('/admin/firm', firm.FirmPage),
        ('/admin/firm_set', firm.FirmForm),
        ('/admin/firm_status', firm.StatusFirmPage),
        ('/admin/project/(.*)', project.ProjectPage),
        ('/admin/project_form', project.ProjectForm),
        ('/admin/image/(.*)/(.*)', image.ImagePage),
        ('/admin/image_form', image.ImageForm),
        ('/img/(.*)/(.*)/(.*)', image.ImageResource),
        
        ('/api/firm/(.*)', firm.FirmApi),
        ('/api/project/(.*)/(.*)', project.ProjectApi)
    ],
    debug=True
    )

