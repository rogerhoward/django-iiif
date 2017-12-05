
from django.db.models import ImageField
from django.db.models.fields.files import ImageFieldFile
from django.conf import settings
from django import template



def urljoin(parts):
    """
    Takes a list of URL parts and smushes em together into a string,
    while ensuring no double slashes, but preserving any trailing slash(es)
    """
    if len(parts) == 0:
        raise ValueError('urljoin needs a list of at least length 1')
    return '/'.join([x.strip('/') for x in parts[0:-1]] + [parts[-1].lstrip('/')])


class IIIFObject(object):
    def __init__(self, parent):
        for name in settings.IIIF_PROFILES:

            profile = settings.IIIF_PROFILES[name]

            if type(profile) is dict:
                iiif = profile
            elif callable(profile):
                iiif = profile(parent)

            url = urljoin([iiif['host'], parent.name, iiif['region'], iiif['size'], iiif['rotation'], '{}.{}'.format(iiif['quality'], iiif['format'])])
            setattr(self, name, url)

        setattr(self, 'url', urljoin([settings.IIIF_HOST, parent.name]))


class IIIFFieldFile(ImageFieldFile):
    @property
    def iiif(self):
        return IIIFObject(self)

    def __init__(self, *args, **kwargs):
        super(IIIFFieldFile, self).__init__(*args, **kwargs)


class IIIFField(ImageField):
    attr_class = IIIFFieldFile

    def __init__(self, *args, **kwargs):
        super(IIIFField, self).__init__(*args, **kwargs)
