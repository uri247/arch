from google.appengine.ext import webapp


class RequestHandler(webapp.RequestHandler):
    def w(self, msg):
        self.response.out.write( msg )
        
    def html_content(self):
        self.response.headers['Content-Type'] = 'text/html'

    def get_firmid(self):
        return 'frl'