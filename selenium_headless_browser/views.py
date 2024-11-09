from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import ParseError
import json
import time
import logging

from selenium_headless_browser.models import CodeLogHistory
from selenium_headless_browser.utils import process_codes_concurrent, filter_major_minor_codes

logger = logging.getLogger(__name__)


class MedicareSearchView(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            body = request.data
            input_numbers = body.get('input_numbers', [])
            match_code = request.query_params.get('match_code', 'false').lower() == 'true'
            start_time = time.perf_counter()
            user = request.user
            results = process_codes_concurrent(input_numbers)
            print("results", results)
            if user.username:
                # Access the first dictionary in the results list
                if results and isinstance(results, list):
                    result_data = results[0]
                    logged_major_codes = set()

                    for result in result_data.get('results', []):
                        major_code = result_data.get('input_number')
                        if major_code not in logged_major_codes:
                            CodeLogHistory.objects.create(
                                user=user,
                                major_code=major_code,
                                result_json=result_data
                            )
                            logged_major_codes.add(major_code)

            if match_code:
                results = filter_major_minor_codes(results, input_numbers)
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
