import model
import main
import web
import json


class FirmPage(web.RequestHandler):
    def get(self, firmid):
        key = model.firm_key( firmid )
        firm = key.get()
        if not firm:
            firm = model.Firm(key=key)
            firm.put()
        projects = model.Project.query_firm(key).fetch()
        
        tmpl = main.jinja_env.get_template( 'admin/firm.html' )
        html = tmpl.render( { 
            'firmid': firmid,
            'firm': firm.to_dict(),
            'projects': projects                 
            } )
        
        self.html_content()
        self.w( html )
        pass


class FirmForm(web.RequestHandler):
    def post(self):
        firmid = self.request.get('firmid')
        firm = model.firm_key( firmid ).get()
        if( firm ):
            #update the firm     
            firm.name_e = self.request.get('name_e')
            firm.name_h = self.request.get('name_h')
            firm.about_e = self.request.get('about_e')
            firm.about_h = self.request.get('about_h')
            firm.put()
            self.redirect('/%s/admin/firm_status' % firmid)
        else:
            self.redirect('/%s/admin/firm' % firmid)


class StatusFirmPage(web.RequestHandler):
    def get(self, firmid):
        tmpl = main.jinja_env.get_template( 'admin/firm_status.html' )
        html = tmpl.render({ 'name_e': firmid })

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


