import logging
import concurrent.futures
from typing import List, Dict, Any, Generator
from dataclasses import dataclass
import requests
from bs4 import BeautifulSoup
import uuid

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
        # Store active sessions to reuse and reduce overhead
        self.sessions = {}

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

        return [[cell.text.strip() for cell in row.find_all('td')] for row in rows[1:]]

    def search_single_code(self, input_number: str) -> SearchResult:
        try:
            # Reuse or create a new session for this input number
            if input_number not in self.sessions:
                self.sessions[input_number] = requests.Session()

            session = self.sessions[input_number]

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
            soup = BeautifulSoup(response.text, 'html.parser')
            results = self._parse_table(soup)

            headers = []
            table_header = soup.find('table', {'id': 'DataGrid1'})
            if table_header:
                headers = [cell.text.strip() for cell in table_header.find_all('tr')[0].find_all('th')]

            return SearchResult(
                input_number=input_number,
                headers=headers,
                data=results
            )

        except Exception as e:
            logger.error(f"Error processing code {input_number}: {str(e)}")
            return SearchResult(
                input_number=input_number,
                headers=[],
                data=[["Code Not Found"]]
            )
        finally:
            # Clean up session after use if needed
            if input_number in self.sessions:
                del self.sessions[input_number]


def process_codes_in_chunks(input_numbers: List[str], chunk_size: int = 5) -> Generator[Dict[str, Any], None, None]:
    processor = MedicareProcessor()
    total_chunks = (len(input_numbers) + chunk_size - 1) // chunk_size

    for i in range(0, len(input_numbers), chunk_size):
        chunk = input_numbers[i:i + chunk_size]
        chunk_results = []

        with concurrent.futures.ThreadPoolExecutor(max_workers=chunk_size) as executor:
            future_to_input = {
                executor.submit(processor.search_single_code, num): num
                for num in chunk
            }

            for future in concurrent.futures.as_completed(future_to_input):
                try:
                    result = future.result()
                    chunk_results.append({
                        'input_number': result.input_number,
                        'headers': result.headers,
                        'data': result.data
                    })
                except Exception as e:
                    input_number = future_to_input[future]
                    chunk_results.append({
                        'input_number': input_number,
                        'headers': [],
                        'data': [["Code Not Found"]]
                    })

        yield {
            'chunk_number': (i // chunk_size) + 1,
            'total_chunks': total_chunks,
            'results': chunk_results
        }


def process_medicare_codes(input_numbers, chunk_size=5):
    stream_id = str(uuid.uuid4())

    return {
        'stream_id': stream_id,
        'url': f'/medicare-stream/{stream_id}/',
        'total_codes': len(input_numbers)
    }