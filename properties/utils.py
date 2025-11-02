from django.core.cache import cache
from .models import Property

def get_all_properties():
    """Retrieve all properties with low-level caching for 1 hour."""
    properties = cache.get('all_properties')
    if properties is None:
        # Cache miss → fetch from DB and store in Redis
        properties = list(
            Property.objects.all().values(
                "id", "title", "description", "price", "location", "created_at"
            )
        )
        cache.set('all_properties', properties, 3600)  # Cache for 1 hour
    return properties

