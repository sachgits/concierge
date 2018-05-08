import uuid
import os
from time import strftime
from urllib.parse import urlencode
from urllib.request import urlopen
from django.conf import settings

def unique_filepath(self, filename):
    pass

def unique_avatar_large_filename(self, filename):
    ext = filename.split('.')[-1]
    filename = str('large.' + ext)
    return unique_avatar_filepath(self.user, filename)  

def unique_avatar_medium_filename(self, filename):
    ext = filename.split('.')[-1]
    filename = str('medium.' + ext)
    return unique_avatar_filepath(self.user, filename)  

def unique_avatar_small_filename(self, filename):
    ext = filename.split('.')[-1]
    filename = str('small.' + ext)
    return unique_avatar_filepath(self.user, filename)  

def unique_avatar_tiny_filename(self, filename):
    ext = filename.split('.')[-1]
    filename = str('tiny.' + ext)
    return unique_avatar_filepath(self.user, filename)  

def unique_avatar_topbar_filename(self, filename):
    ext = filename.split('.')[-1]
    filename = str('topbar.' + ext)
    return unique_avatar_filepath(self.user, filename)  
    
def unique_avatar_filepath(self, filename):
    result = os.path.join('avatars/', strftime('%Y/%m/%d'), str(self.id), filename)
    return result

def unique_idp_metadata_filepath(self, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    result = os.path.join('idp_metadata/', filename)
    return result

