import jinja2
import os
from google.appengine.ext import webapp
import admin
import home
import projects
import testpage

static_dir =  os.path.join( os.path.dirname(__file__), 'templates' )
jinja_env = jinja2.Environment( loader=jinja2.FileSystemLoader( static_dir ) )


class MainPage(webapp.RequestHandler):
    def get(self):
        #self.redirect( '/frl/h/about' )
        self.redirect('/static/static-home.html')

class MainAdminPage(webapp.RequestHandler):
    def get(self):
        self.redirect( '/frl/admin/firm' )
                

application = webapp.WSGIApplication(
    [
        ('/', MainPage),
        ('/admin', MainAdminPage),

        ('/(.*)/(.*)/home', home.HomePage ),
        ('/(.*)/(.*)/projects', projects.ProjectsPage ),
        ('/(.*)/(.*)/test', testpage.TestPage ),


        ('/(.*)/admin/firm', admin.FirmPage),
        ('/(.*)/admin/firm_status', admin.StatusFirmPage),
        ('/(.*)/admin/project/(.*)', admin.ProjectPage),
        ('/(.*)/admin/image/(.*)/', admin.UploadImagesPage),
        ('/(.*)/admin/image/(.*)/(.+)', admin.ImagePage),

        ('/form/firm', admin.FirmForm),
        ('/form/project', admin.ProjectForm),
        ('/form/image', admin.ImageForm),

        ('/img/(.*)/(.*)/(.*)', admin.ImageResource),

        ('/api/firm/(.*)', admin.FirmApi),
        ('/api/project/(.*)/(.*)', admin.ProjectApi),
        ('/api/get-upload-url/(.*)/(.*)', admin.GetUploadUrlApi),
    ],
    debug=True
)
