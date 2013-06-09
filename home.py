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
        lfirm = literals.localize( firm.to_dict(), lang );

        if( not firm ):
            self.error(500)
        else:
            tmpl = main.jinja_env.get_template( 'base.html' )
            html = tmpl.render({
                'firm': lfirm,
                'ctx_menu': menu, 
                'trans_text': lfirm['about'],
            })
            self.html_content()
            self.w( html )

