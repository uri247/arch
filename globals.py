import jinja2
import os

static_dir = os.path.join( os.path.dirname(__file__), 'templates' )
jinja_env = jinja2.Environment( loader=jinja2.FileSystemLoader( static_dir ) )

