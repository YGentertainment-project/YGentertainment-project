from import_export import resources
from .models import *


class PlatformResource(resources.ModelResource):
    class Meta:
        model = Platform
