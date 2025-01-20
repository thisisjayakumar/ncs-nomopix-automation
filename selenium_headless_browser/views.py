from django.http import StreamingHttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import ParseError

import json
import time
import logging
import concurrent.futures
from typing import List, Dict, Generator
from django.views import View

from selenium_headless_browser.models import CodeLogHistory
from selenium_headless_browser.utils import process_codes_in_chunks
from .helpers import load_env, get_auth_token, save_auth_token, delete_test

logger = logging.getLogger(__name__)


class MedicareSearchView(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Handle POST requests for Medicare code search with advanced streaming and caching
        """
        try:
            # Extract query parameters
            match_code = request.GET.get('match_code', 'false').lower() == 'true'

            # Validate and extract request data
            body = request.data
            input_numbers = body.get('input_numbers', [])
            chunk_size = body.get('chunk_size', 5)
            stream_results = body.get('stream_results', True)
            max_workers = body.get('max_workers', min(len(input_numbers), 10))  # Configurable thread count

            # Validate input
            if not input_numbers:
                return JsonResponse({'error': 'No input numbers provided'}, status=400)

            start_time = time.perf_counter()
            user = request.user

            # Choose response method based on streaming preference
            if stream_results:
                return self._stream_response(
                    user,
                    input_numbers,
                    chunk_size,
                    start_time,
                    max_workers,
                    match_code
                )
            else:
                return self._bulk_response(
                    user,
                    input_numbers,
                    chunk_size,
                    start_time,
                    max_workers,
                    match_code
                )

        except json.JSONDecodeError:
            raise ParseError(detail="Invalid JSON in request body")
        except Exception as e:
            logger.error(f"Error processing request: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)

    def _get_cached_results(self, user, input_numbers: List[str], match_code: bool = False) -> tuple:
        if not user.username or user.subscription not in [2, 3]:
            return [], input_numbers

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

        return cached_results, uncached_numbers

    def _process_chunk_with_caching(self, user, chunk: List[str], match_code: bool = False) -> List[Dict]:
        """
        Process a chunk of codes with optional caching for premium users
        """
        # Pass match_code to process_codes_in_chunks if needed
        chunk_results = list(process_codes_in_chunks(chunk, len(chunk), match_code=match_code))

        if user.username and user.subscription in [2, 3]:
            for result in chunk_results[0]['results']:
                CodeLogHistory.objects.create(
                    user=user,
                    major_code=result['input_number'],
                    result_json=result
                )

        return chunk_results[0]['results']

    def _stream_response(self, user, input_numbers, chunk_size, start_time, max_workers, match_code=False):
        """
        Create a streaming HTTP response
        """

        def results_generator() -> Generator:
            try:
                # Get cached results first
                cached_results, uncached_numbers = self._get_cached_results(user, input_numbers, match_code)

                # Yield cached results first
                for result in cached_results:
                    yield f"data: {json.dumps({'type': 'cached', 'result': result})}\n\n"

                # Process remaining numbers using multithreading
                with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
                    # Split uncached numbers into chunks
                    chunks = [uncached_numbers[i:i + chunk_size] for i in range(0, len(uncached_numbers), chunk_size)]

                    for chunk_index, chunk in enumerate(chunks, 1):
                        # Submit chunk processing to thread pool
                        future = executor.submit(self._process_chunk_with_caching, user, chunk, match_code)
                        chunk_results = future.result()

                        processed_chunk = {
                            'chunk_number': chunk_index,
                            'total_chunks': len(chunks),
                            'results': chunk_results
                        }

                        yield f"data: {json.dumps(processed_chunk)}\n\n"

                # Send completion message
                elapsed_time = time.perf_counter() - start_time
                yield f"data: {json.dumps({'status': 'completed', 'elapsed_time': f'{elapsed_time:.6f} seconds'})}\n\n"

            except Exception as e:
                yield f"data: {json.dumps({'status': 'error', 'message': str(e)})}\n\n"

        # Create streaming response
        response = StreamingHttpResponse(
            streaming_content=results_generator(),
            content_type='text/event-stream'
        )
        response['Cache-Control'] = 'no-cache'
        response['X-Accel-Buffering'] = 'no'
        response['Content-Type'] = 'text/event-stream'
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response

    def _bulk_response(self, user, input_numbers, chunk_size, start_time, max_workers, match_code=False):
        results = []

        cached_results, uncached_numbers = self._get_cached_results(user, input_numbers, match_code)
        results.extend(cached_results)

        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            chunks = [uncached_numbers[i:i + chunk_size] for i in range(0, len(uncached_numbers), chunk_size)]

            for chunk in chunks:
                future = executor.submit(self._process_chunk_with_caching, user, chunk, match_code)
                chunk_results = future.result()
                results.extend(chunk_results)

        elapsed_time = time.perf_counter() - start_time
        return JsonResponse({
            'results': results,
            'elapsed_time': f"{elapsed_time:.6f} seconds"
        })

    def options(self, request, *args, **kwargs):
        response = JsonResponse({})
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response

    def get(self, request, *args, **kwargs):
        return JsonResponse({'error': 'Only POST method is allowed'}, status=405)


class CancelTestsView(APIView):
    @csrf_exempt
    def post(self, request):
        load_env()

        try:
            data = json.loads(request.body)
            test_ids = json.loads(data.get("testId", "[]"))
            auth_token = data.get("authToken")

            # Use stored auth token if not provided
            if not auth_token:
                auth_token = get_auth_token()
                if not auth_token:
                    return JsonResponse({"error": "No authToken provided."}, status=400)

            if data.get("authToken"):
                save_auth_token(auth_token)

            results = {}
            for test_id in test_ids:
                response = delete_test(test_id, auth_token)

                if response.status_code != 200:
                    return JsonResponse({"error": "Please provide a new authToken."}, status=403)

                results[test_id] = {
                    "status": response.status_code,
                    "body": response
                }

            return JsonResponse(results, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format."}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)