from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .utils import search_query_script

@csrf_exempt
def run_selenium(request):
    if request.method == "POST":
        try:
            # Extract input numbers from the request body
            body = json.loads(request.body)
            input_numbers = body.get('input_numbers', [])

            # Check for match_code query param
            match_code = request.GET.get('match_code', 'false').lower() == 'true'

            # Run the selenium queries concurrently
            results = search_query_script(input_numbers)

            if match_code:
                # If match_code=true, filter the results based on major/minor code logic
                filtered_results = filter_major_minor_codes(results, input_numbers)
                return JsonResponse({'results': filtered_results}, safe=False)

            # Otherwise, return the full unfiltered results
            return JsonResponse({'results': results}, safe=False)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        
        
def filter_major_minor_codes(results, input_numbers):
    """
    Filters results by checking if minor codes of each major code exist in the input_numbers.
    If a match is found, return the full row with headers.
    """
    filtered_results = []

    # Convert input_numbers to string to match data type with results
    input_numbers_str = [str(num) for num in input_numbers]

    for result in results:
        input_number = result['input_number']
        result_data = result['results']

        if not result_data or result_data[0] == ["Code Not Found"]:
            continue  # Skip if no data

        major_code = str(input_number)  # Major code is the input number itself
        matching_rows = []

        # Header for the result table
        headers = result_data[0]  # The first row should be the header

        # Loop through result data to find matching minor codes
        for row in result_data[1:]:
            minor_code = row[1]  # Minor code is in the second column
            if minor_code in input_numbers_str:  # Check if the minor code is in input numbers
                # If match found, include the full row (with headers)
                matching_rows.append({
                    'major_code': major_code,
                    'minor_code': minor_code,
                    'data': row  # Return the full row data including headers
                })

        # If there are matching rows, append to the filtered result
        if matching_rows:
            filtered_results.append({
                'input_number': major_code,
                'headers': headers,  # Include the headers in the result
                'results': matching_rows
            })

    return filtered_results
