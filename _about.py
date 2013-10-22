from google.appengine.ext import ndb
import main
import web
from literals import localize, about_menu, get_attr


class AboutPage(web.RequestHandler):    
    def get(self,firmid,lang):
        self.html_content()

        firm_key = ndb.Key( "Firm", firmid )
        firm = firm_key.get()
        if( not firm ):
            self.error(500)
            return
        
        menu = localize( about_menu, lang );

        tmpl = main.jinja_env.get_template( 'about.html' )
        html = tmpl.render({
            'firmid': firmid,
            'firm': localize(firm.to_dict(),lang),
            'ctx_menu': menu, 
            'trans_head': get_attr( firm, lang, 'name' ),
            'trans_text': get_attr( firm, lang, 'about' ),
        })
        
        self.html_content()
        self.w( html )

