from django.core.cache import cache
from django.http import JsonResponse


class CachePostRequestsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == 'POST':
            match_code = request.headers.get('matchCode', None)
            cache_key = f"post_cache_{hash((request.body, match_code))}"
            cached_response = cache.get(cache_key)

            if cached_response:
                return JsonResponse(cached_response)
            response = self.get_response(request)
            cache.set(cache_key, response.json(), timeout=60 * 1440)
            return response

        return self.get_response(request)
