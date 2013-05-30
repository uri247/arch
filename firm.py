from google.appengine.ext import ndb
import model
import main
import web


class FirmPage(web.RequestHandler):
    def get(self):        
        key = ndb.Key( "Firm", self.get_firmid() )
        firm = key.get()
        if( not firm ):
            firm = model.Firm(key=key,name_e='',name_h='')
            firm.put()
                    
        tmpl = main.jinja_env.get_template( 'firm.html' )
        html = tmpl.render( { 
            'key_name': self.get_firmid(),
            'name_e': firm.name_e,
            'name_h': firm.name_h,                 
            } )
        
        self.html_content()
        self.w( html )
        pass


class SetFirmPage(web.RequestHandler):
    def post(self):
        key_name = self.request.get('key_name')
        firm = ndb.Key( "Firm", key_name ).get()
        if( firm ):
            #update the firm     
            firm.name_e = self.request.get('name_e')
            firm.name_h = self.request.get('name_h')
            firm.put()
            self.redirect('/firm_status')
        else:
            self.redirect('/firm')


class StatusFirmPage(web.RequestHandler):
    def get(self):
        tmpl = main.jinja_env.get_template( 'firm_status.html' )
        html = tmpl.render({ 'name_e': self.get_firmid() })

        self.html_content()
        self.w( html )



