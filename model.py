from google.appengine.ext import ndb
from google.appengine.api.images import get_serving_url


class Firm(ndb.Model):
    name_e = ndb.StringProperty()
    name_h = ndb.StringProperty()
    about_e = ndb.StringProperty()
    about_h = ndb.StringProperty()


class Project(ndb.Model):
    """Project
    A model to describe an architecture project performed by a Firm
    """
    title_e = ndb.StringProperty()
    title_h = ndb.StringProperty()
    address_e = ndb.StringProperty()
    address_h = ndb.StringProperty()
    year = ndb.IntegerProperty()
    classification = ndb.StringProperty()
    classification2 = ndb.StringProperty()
    plot_area = ndb.IntegerProperty()
    built_area = ndb.IntegerProperty()
    units = ndb.StringProperty()
    status = ndb.StringProperty()
    description_e = ndb.StringProperty()
    description_h = ndb.StringProperty()
    front_picture = ndb.StringProperty()

    @classmethod
    def query_firm(cls, firm_key):
        return cls.query( ancestor=firm_key ).order(-cls.year)
            

class Image(ndb.Model):
    """Image
    an image. may be related to a project or to a person
    """
    name = ndb.StringProperty()
    mime_type = ndb.StringProperty()
    blob_key = ndb.BlobKeyProperty()

    def to_dict(self, include=None, exclude=None, size=None):
        """calls the super method, and add a URL
        :param include: set of property names to include, default all
        :param exclude: set of property names to exclude, default none
        :param size: the size of the image. default None (original size)
        :return:
        """
        d = super(Image, self).to_dict(include=include, exclude=exclude)
        d['url'] = get_serving_url(self.blob_key, size=size)
        d['id'] = self.key.id()
        return d
        pass


def firm_key(firmid):
    """Generate a NDB key from firmid
    :param firmid: firm id (e.g. frl)
    """
    return ndb.Key( "Firm", firmid )