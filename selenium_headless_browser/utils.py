import concurrent.futures
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())


def setup_driver():
    """Initializes the Chrome driver with options."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(options=chrome_options)
    return driver


def accept_license(driver):
    """Accept the license agreement."""
    try:
        accept_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "Accept"))
        )
        accept_button.click()
        print("License agreement accepted.")
    except Exception as e:
        print("Error accepting license agreement:", e)


def perform_search(driver, input_number):
    """Perform a search for a given input number and return the results."""
    try:
        search_input = driver.find_element(By.NAME, "txtProcCode")
        search_input.clear()
        search_input.send_keys(str(input_number))

        search_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "Button1"))
        )
        search_button.click()

        wait = WebDriverWait(driver, 5)
        table = wait.until(EC.presence_of_element_located((By.ID, "DataGrid1")))
        
        if table:
            return parse_table(table)
        else:
            return [["Code Not Found"]]
    
    except Exception as e:
        print(f"Error searching for {input_number}: {e}")
        return [["Code Not Found"]]


def parse_table(table):
    """Parses the result table and extracts rows of data, excluding header if no data is present."""
    rows = table.find_elements(By.TAG_NAME, "tr")
    current_results = []
    
    if len(rows) > 1:
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            row_data = [cell.text for cell in cells]
            current_results.append(row_data)
        
        return current_results
    else:
        return [["Code Not Found"]]


def search_single_input(input_number):
    """Each search will have its own WebDriver instance."""
    driver = setup_driver()  # Setup a new WebDriver instance
    driver.get("https://www.cgsmedicare.com/medicare_dynamic/j15/ptpb/ptp/ptp.aspx")
    accept_license(driver)  # Accept the license agreement

    time.sleep(2)  # Add a delay between searches
    result = perform_search(driver, input_number)
    
    driver.quit()  # Quit WebDriver instance after task
    return {
        'input_number': input_number,
        'results': result
    }


def search_query_script(input_numbers):
    start_time = time.perf_counter()
    
    results = []
    
    # Parallelize searches using thread pool executor
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_input = {executor.submit(search_single_input, num): num for num in input_numbers}
        for future in concurrent.futures.as_completed(future_to_input):
            input_number = future_to_input[future]
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                print(f"Search failed for {input_number}: {e}")
                results.append({
                    'input_number': input_number,
                    'results': [["Code Not Found"]]
                })
    
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time:.6f} seconds")
    return results
