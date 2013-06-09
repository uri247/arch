import jinja2
import os
from google.appengine.ext import webapp
import admin
import home

static_dir =  os.path.join( os.path.dirname(__file__), 'templates' )
jinja_env = jinja2.Environment( loader=jinja2.FileSystemLoader( static_dir ) )


class MainPage(webapp.RequestHandler):
    def get(self):
        self.redirect( '/static/sample-ashdod.html' )
        
class AdminPage(webapp.RequestHandler):
    def get(self):
        self.redirect( '/admin/firm' )


application = webapp.WSGIApplication([
        ('/', MainPage),
        ('/home', home.HomePage),
        
        ('/admin', AdminPage),
        ('/admin/firm', admin.FirmPage),
        ('/admin/firm_set', admin.FirmForm),
        ('/admin/firm_status', admin.StatusFirmPage),
        ('/admin/project/(.*)/(.*)', admin.ProjectPage),
        ('/admin/project_form', admin.ProjectForm),
        ('/admin/image/(.*)/(.*)/(.*)', admin.ImagePage),
        ('/admin/image_form', admin.ImageForm),
        
        ('/img/(.*)/(.*)/(.*)', admin.ImageResource),
        
        ('/api/firm/(.*)', admin.FirmApi),
        ('/api/project/(.*)/(.*)', admin.ProjectApi)
    ],
    debug=True
    )

