import logging
import concurrent.futures
from typing import List, Dict, Any
from dataclasses import dataclass
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


@dataclass
class SearchResult:
    input_number: str
    headers: List[str]
    data: List[List[str]]


class MedicareProcessor:
    def __init__(self):
        self.base_url = "https://www.cgsmedicare.com/medicare_dynamic/j15/ptpb/ptp/ptp.aspx"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def _get_form_data(self, response_text: str) -> Dict[str, str]:
        """Extract hidden form fields from the page."""
        soup = BeautifulSoup(response_text, 'html.parser')
        return {
            '__VIEWSTATE': soup.find('input', {'id': '__VIEWSTATE'})['value'],
            '__VIEWSTATEGENERATOR': soup.find('input', {'id': '__VIEWSTATEGENERATOR'})['value'],
            '__EVENTVALIDATION': soup.find('input', {'id': '__EVENTVALIDATION'})['value']
        }

    def _parse_table(self, soup: BeautifulSoup) -> List[List[str]]:
        """Parse the results table from the response."""
        table = soup.find('table', {'id': 'DataGrid1'})
        if not table:
            return [["Code Not Found"]]

        rows = table.find_all('tr')
        if len(rows) <= 1:
            return [["Code Not Found"]]

        return [[cell.text.strip() for cell in row.find_all('td')] for row in rows]

    def search_single_code(self, input_number: str) -> SearchResult:
        """Process a single procedure code."""
        try:
            session = requests.Session()

            # Initial page load
            response = session.get(self.base_url, headers=self.headers)
            form_data = self._get_form_data(response.text)

            # Accept license
            form_data['Accept'] = 'Accept'
            session.post(self.base_url, data=form_data, headers=self.headers)

            # Perform search
            form_data = self._get_form_data(response.text)
            form_data.update({
                'txtProcCode': str(input_number),
                'Button1': 'Search'
            })

            response = session.post(self.base_url, data=form_data, headers=self.headers)
            results = self._parse_table(BeautifulSoup(response.text, 'html.parser'))

            headers = results[0] if results and results[0] != ["Code Not Found"] else []
            data = results[1:] if results and results[0] != ["Code Not Found"] else results

            return SearchResult(
                input_number=input_number,
                headers=headers,
                data=data
            )

        except Exception as e:
            logger.error(f"Error processing code {input_number}: {str(e)}")
            return SearchResult(
                input_number=input_number,
                headers=[],
                data=[["Code Not Found"]]
            )


def process_codes_concurrent(input_numbers: List[str]) -> List[Dict[str, Any]]:
    """Process multiple codes concurrently."""
    processor = MedicareProcessor()
    results = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_input = {
            executor.submit(processor.search_single_code, num): num
            for num in input_numbers
        }

        for future in concurrent.futures.as_completed(future_to_input):
            try:
                result = future.result()
                results.append({
                    'input_number': result.input_number,
                    'headers': result.headers,
                    'results': result.data
                })
            except Exception as e:
                input_number = future_to_input[future]
                logger.error(f"Failed to process {input_number}: {str(e)}")
                results.append({
                    'input_number': input_number,
                    'headers': [],
                    'results': [["Code Not Found"]]
                })

    return results