import jinja2
import os
from google.appengine.ext import webapp
import admin
import home
import about
import contact
import projects
import testpage

static_dir = os.path.join( os.path.dirname(__file__), 'templates' )
jinja_env = jinja2.Environment( loader=jinja2.FileSystemLoader( static_dir ) )


class MainPage(webapp.RequestHandler):
    def get(self):
        self.redirect( '/frl/h/home' )

class MainAdminPage(webapp.RequestHandler):
    def get(self):
        self.redirect( '/frl/admin/firm' )

class GoLang(webapp.RequestHandler):
    def get(self, firm, lang, tolang):
        self.redirect( '/frl/h/home')

application = webapp.WSGIApplication(
    [
        ('/', MainPage),
        ('/admin', MainAdminPage),

        ('/(.*)/(h|e)/home', home.HomePage ),
        ('/(.*)/(h|e)/about', about.AboutPage),
        ('/(.*)/(h|e)/projects', projects.ProjectsPage),
        ('/(.*)/(h|e)/contact', contact.ContactPage),
        ('/(.*)/(h|e)/go-(he|en)', GoLang),
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
