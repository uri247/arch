import jinja2
import os
from google.appengine.ext import webapp
import firm
import project

static_dir =  os.path.join( os.path.dirname(__file__), 'static' )
jinja_env = jinja2.Environment( loader=jinja2.FileSystemLoader( static_dir ) )


class MainPage(webapp.RequestHandler):
    def get(self):
        self.redirect( '/admin/firm' )
        


application = webapp.WSGIApplication([
        ('/', MainPage),
        ('/admin/firm', firm.FirmPage),
        ('/admin/firm_set', firm.SetFirmPage),
        ('/admin/firm_status', firm.StatusFirmPage),
        ('/admin/project/(.*)', project.ProjectPage),
    ],
    debug=True
    )

