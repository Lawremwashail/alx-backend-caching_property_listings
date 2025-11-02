from django.core.cache import cache
from .models import Property
from django_redis import get_redis_connection
import logging

logger = logging.getLogger(__name__)

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


def get_redis_cache_metrics():
    """Retrieve Redis cache hit/miss metrics and calculate hit ratio."""
    try:
        # Connect to Redis through django_redis
        redis_conn = get_redis_connection("default")

        # Retrieve Redis INFO stats
        info = redis_conn.info()

        hits = info.get("keyspace_hits", 0)
        misses = info.get("keyspace_misses", 0)

        total = hits + misses
        hit_ratio = (hits / total) if total > 0 else 0.0

        metrics = {
            "hits": hits,
            "misses": misses,
            "hit_ratio": round(hit_ratio, 2),
        }

        logger.info(f"Redis Cache Metrics: {metrics}")
        return metrics

    except Exception as e:
        logger.error(f"Error fetching Redis metrics: {e}")
        return {"error": str(e)}
