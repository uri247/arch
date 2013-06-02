from google.appengine.ext import webapp


class RequestHandler(webapp.RequestHandler):
    def w(self, msg):
        self.response.out.write( msg )
        
    def html_content(self):
        self.response.headers['Content-Type'] = 'text/html'
        
    def json_content(self):
        self.response.headers['Content-Type'] = 'application/javascript'

    def get_firmid(self):
        return 'frl'