from google.appengine.ext import ndb


class Firm(ndb.Model):
    name_e = ndb.StringProperty()
    name_h = ndb.StringProperty()


class Project(ndb.Model):
    """Project
    A model to describe an architecture project performed by a Firm
    """
    title_e = ndb.StringProperty()
    title_h = ndb.StringProperty()
    address_e = ndb.StringProperty()
    address_h = ndb.StringProperty()
    year = ndb.IntegerProperty()
    description_e = ndb.StringProperty()
    description_h = ndb.StringProperty()
    status = ndb.StringProperty()
    plot_area = ndb.IntegerProperty()
    built_area = ndb.IntegerProperty()
    classification = ndb.StringProperty()
