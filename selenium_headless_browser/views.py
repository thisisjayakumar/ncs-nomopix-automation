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
            user = request.user if request.user.is_authenticated else None
            results = process_codes_concurrent(input_numbers)
            if user:
                for result in results.get('results', []):
                    major_code = result.get('input_number')
                    CodeLogHistory.objects.create(
                        user=user,
                        major_code=major_code,
                        result_json=result
                    )

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
