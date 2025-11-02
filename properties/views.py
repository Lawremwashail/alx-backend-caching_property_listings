from django.http import JsonResponse
from .utils import get_all_properties

def property_list(request):
    """Return cached list of all properties using Redis low-level cache."""
    properties = get_all_properties()
    return JsonResponse({"data": properties}, safe=False)

