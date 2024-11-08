from django.core.cache import cache
from django.http import JsonResponse


class CachePostRequestsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == 'POST' and request.path in ['/run-query/search-query/']:
            match_code = request.headers.get('match_code', None)
            cache_key = f"post_cache_{hash((request.body, match_code))}"
            cached_response = cache.get(cache_key)

            if cached_response:
                return JsonResponse(cached_response, safe=False)

            response = self.get_response(request)
            if isinstance(response, JsonResponse):
                cache.set(cache_key, response.content.decode('utf-8'), timeout=60 * 1440)

            return response

        return self.get_response(request)
