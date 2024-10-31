from nis import match

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import time
import logging
from selenium_headless_browser.utils import process_codes_concurrent, filter_major_minor_codes

logger = logging.getLogger(__name__)


@csrf_exempt
def run_medicare_search(request):
    if request.method != "POST":
        return JsonResponse({'error': 'Only POST method is allowed'}, status=405)

    try:
        body = json.loads(request.body)
        input_numbers = body.get('input_numbers', [])
        match_code = request.GET.get('matchCode', 'false').lower() == 'true'

        start_time = time.perf_counter()
        results = process_codes_concurrent(input_numbers)
        print("match_code: ", match_code)
        if match_code:
            results = filter_major_minor_codes(results, input_numbers)

        end_time = time.perf_counter()
        elapsed_time = end_time - start_time

        return JsonResponse({
            'results': results,
            'elapsed_time': f"{elapsed_time:.6f} seconds"
        })

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON in request body'}, status=400)
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)

