import model
import main
import web
import literals

class HomePage(web.RequestHandler):
    def get(self):
        self.html_content()
                
        key = model.firm_key( self.get_firmid() )
        firm = key.get()
        lang = 'h'
        menu = literals.localize( literals.about_menu, lang );

        if( not firm ):
            self.error(500)
        else:
            tmpl = main.jinja_env.get_template( 'home.html' )
            html = tmpl.render({
                'firm': { 'name': firm.name_h },
                #'ctx_menu': literals.localize( literals.about_menu, lang )
                'ctx_menu': menu, 
            })
            self.html_content()
            self.w( html )

