from import_export import resources
from .models import Platform


class PlatformResource(resources.ModelResource):
    class Meta:
        model = Platform
