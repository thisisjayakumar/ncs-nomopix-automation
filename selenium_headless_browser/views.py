from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import ParseError
import json
import time
import logging

from selenium_headless_browser.models import CodeLogHistory
from selenium_headless_browser.utils import process_codes_concurrent

logger = logging.getLogger(__name__)


class MedicareSearchView(APIView):
    # authentication_classes = [JWTAuthentication]
    permission_classes = []

    def post(self, request, *args, **kwargs):
        try:
            body = request.data
            input_numbers = body.get('input_numbers', [])
            start_time = time.perf_counter()
            user = request.user
            results = []
            if user.username and user.subscription in [2, 3]:
                cached_results = []
                uncached_numbers = []

                for number in input_numbers:
                    try:
                        log_entry = CodeLogHistory.objects.get(
                            user=user,
                            major_code=number
                        )
                        cached_results.append(log_entry.result_json)
                    except CodeLogHistory.DoesNotExist:
                        uncached_numbers.append(number)

                if uncached_numbers:
                    new_results = process_codes_concurrent(uncached_numbers)
                    results = cached_results + new_results

                    for result in new_results:
                        if isinstance(result, dict):
                            major_code = result.get('input_number')
                            CodeLogHistory.objects.create(
                                user=user,
                                major_code=major_code,
                                result_json=result
                            )
                else:
                    results = cached_results
            else:
                results = process_codes_concurrent(input_numbers)

            elapsed_time = time.perf_counter() - start_time

            return JsonResponse({
                'results': results,
                'elapsed_time': f"{elapsed_time:.6f} seconds"
            })

        except json.JSONDecodeError:
            raise ParseError(detail="Invalid JSON in request body")
        except Exception as e:
            logger.error(f"Error processing request: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)

    def get(self, request, *args, **kwargs):
        return JsonResponse({'error': 'Only POST method is allowed'}, status=405)
