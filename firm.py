import model
import main
import web
import json


class FirmPage(web.RequestHandler):
    def get(self):        
        key = model.firm_key( self.get_firmid() )
        firm = key.get()
        if( not firm ):
            firm = model.Firm(key=key,name_e='',name_h='')
            firm.put()
        projects = model.Project.query_firm(key).fetch()
                    
        tmpl = main.jinja_env.get_template( 'firm.html' )
        html = tmpl.render( { 
            'key_name': self.get_firmid(),
            'name_e': firm.name_e,
            'name_h': firm.name_h,
            'projects': projects                 
            } )
        
        self.html_content()
        self.w( html )
        pass


class FirmForm(web.RequestHandler):
    def post(self):
        key_name = self.request.get('key_name')
        firm = model.firm_key( key_name ).get()
        if( firm ):
            #update the firm     
            firm.name_e = self.request.get('name_e')
            firm.name_h = self.request.get('name_h')
            firm.put()
            self.redirect('firm_status')
        else:
            self.redirect('firm')


class StatusFirmPage(web.RequestHandler):
    def get(self):
        tmpl = main.jinja_env.get_template( 'firm_status.html' )
        html = tmpl.render({ 'name_e': self.get_firmid() })

        self.html_content()
        self.w( html )


class FirmApi(web.RequestHandler):
    def get(self, firmid):
        """returns a firm with firmid"""
        key = model.firm_key( firmid )
        firm = key.get()
        if( not firm ):
            self.error(404)
        else:
            js = json.dumps( firm.to_dict() )        
            self.json_content()
            self.w( js )

    def post(self, firmid):
        """create a new firm"""
        firm = model.Firm.get_by_id(firmid)
        if( firm ):
            #firm already exists. returns conflict
            self.error(409)
        else:
            d = json.loads( self.request.body )
            firm = model.Firm( key = model.firm_key(firmid), **d )
            firm.put()
            
    def put(self, firmid):
        firm = model.Firm.get_by_id(firmid)
        if( not firm ):
            self.error(404)
        else:
            d = json.loads( self.request.body )
            firm.populate( **d )
            firm.put()

    def delete(self, firmid):
        firm = model.Firm.get_by_id(firmid)
        if( not firm ):
            self.error(404)
        else:
            firm.key.delete()


