#!/usr/bin/env python3
"""
ACRIS (Automated City Register Information System) Scraper
NYC Property Records Search with Anti-Bot Protection
"""

import random
import time
import hashlib
from typing import List, Dict, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import html5lib
import re

try:
    import undetected_chromedriver as uc
    UC_AVAILABLE = True
except ImportError:
    UC_AVAILABLE = False

from .anti_bot_scraper import AntiBotScraper


class ACRISScraper(AntiBotScraper):
    """Specialized scraper for NYC ACRIS property records"""

    ACRIS_BASE_URL = "https://a836-acris.nyc.gov/CP/"
    ACRIS_SEARCH_URL = "https://a836-acris.nyc.gov/CP/"

    def __init__(self, captcha_api_key: Optional[str] = None):
        super().__init__(captcha_api_key)
        self.acris_session_id = None

    def _extract_data(self, soup: BeautifulSoup, page_num: int) -> List[Dict]:
        """Extract ACRIS property record data"""
        results = []

        # ACRIS search results are typically in tables
        tables = soup.find_all('table')

        for table in tables:
            rows = table.find_all('tr')
            if len(rows) < 2:  # Skip header-only tables
                continue

            # Extract header row
            headers = []
            header_row = rows[0]
            for th in header_row.find_all(['th', 'td']):
                headers.append(th.get_text(strip=True))

            # Extract data rows
            for row in rows[1:]:
                cells = row.find_all(['td', 'th'])
                if len(cells) == 0:
                    continue

                record = {}
                for idx, cell in enumerate(cells):
                    if idx < len(headers):
                        key = headers[idx] if headers[idx] else f"field_{idx}"
                        value = cell.get_text(strip=True)
                        # Extract links if present
                        link = cell.find('a')
                        if link and link.get('href'):
                            record[f"{key}_link"] = link.get('href')
                        record[key] = value

                if record:
                    record['page'] = page_num
                    results.append(record)

        # Also look for property details in divs/spans
        property_divs = soup.select('div.property-info, div.record-info, span.property-detail')
        for div in property_divs:
            text = div.get_text(strip=True)
            if text and len(text) > 10:  # Meaningful content
                results.append({
                    'property_info': text,
                    'page': page_num,
                    'source': 'div'
                })

        return results

    def search_by_block_lot(self, borough: str, block: str, lot: str, seed: Optional[int] = None) -> List[Dict]:
        """
        Search ACRIS by Block and Lot number

        Args:
            borough: NYC borough (1=Manhattan, 2=Bronx, 3=Brooklyn, 4=Queens, 5=Staten Island)
            block: Block number
            lot: Lot number
            seed: Random seed for timing
        """
        if seed is None:
            seed = self.master_seed

        url = f"{self.ACRIS_BASE_URL}?menuchoice=BL"
        results = []

        driver = self._create_driver()

        try:
            # Random delay before starting
            self._random_delay(1.0, 3.0, seed)

            driver.get(url)

            # Human-like mouse movement
            self._human_like_mouse_movement(driver)

            # Random delay after page load
            self._random_delay(2.0, 5.0, seed)

            # Check for CAPTCHA
            self._handle_captcha(driver, seed)

            # Wait for form to load
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.NAME, "borough"))
            )

            # Fill in borough
            borough_select = Select(driver.find_element(By.NAME, "borough"))
            borough_select.select_by_value(str(borough))
            self._random_delay(0.5, 1.5, seed)

            # Fill in block
            block_input = driver.find_element(By.NAME, "block")
            block_input.clear()
            block_input.send_keys(str(block))
            self._random_delay(0.5, 1.5, seed)

            # Fill in lot
            lot_input = driver.find_element(By.NAME, "lot")
            lot_input.clear()
            lot_input.send_keys(str(lot))
            self._random_delay(1.0, 2.0, seed)

            # Human-like mouse movement before submit
            self._human_like_mouse_movement(driver)

            # Submit form
            submit_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit'], button[type='submit']")
            submit_button.click()

            # Wait for results
            self._random_delay(2.0, 4.0, seed)

            WebDriverWait(driver, 30).until(
                lambda d: d.execute_script('return document.readyState') == 'complete'
            )

            # Human-like scrolling
            self._human_like_scroll(driver, seed)

            # Extract results
            html = driver.page_source
            soup = BeautifulSoup(html, 'html5lib')
            results = self._extract_data(soup, 1)

            # Add search parameters to results
            for result in results:
                result['search_type'] = 'block_lot'
                result['borough'] = borough
                result['block'] = block
                result['lot'] = lot

            return results

        finally:
            driver.quit()

    def search_by_address(self, address: str, borough: Optional[str] = None, seed: Optional[int] = None) -> List[Dict]:
        """
        Search ACRIS by property address

        Args:
            address: Property address (e.g., "123 Main Street")
            borough: Optional borough filter
            seed: Random seed for timing
        """
        if seed is None:
            seed = self.master_seed

        url = f"{self.ACRIS_BASE_URL}?menuchoice=ADDR"
        results = []

        driver = self._create_driver()

        try:
            # Random delay before starting
            self._random_delay(1.0, 3.0, seed)

            driver.get(url)

            # Human-like mouse movement
            self._human_like_mouse_movement(driver)

            # Random delay after page load
            self._random_delay(2.0, 5.0, seed)

            # Check for CAPTCHA
            self._handle_captcha(driver, seed)

            # Wait for form to load
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.NAME, "street_name"))
            )

            # Parse address
            address_parts = self._parse_address(address)

            # Fill in street name
            street_input = driver.find_element(By.NAME, "street_name")
            street_input.clear()
            street_input.send_keys(address_parts.get('street', ''))
            self._random_delay(0.5, 1.5, seed)

            # Fill in house number if available
            if 'house_number' in address_parts:
                house_input = driver.find_element(By.NAME, "house_number")
                house_input.clear()
                house_input.send_keys(address_parts['house_number'])
                self._random_delay(0.5, 1.5, seed)

            # Select borough if provided
            if borough:
                borough_select = Select(driver.find_element(By.NAME, "borough"))
                borough_select.select_by_value(str(borough))
                self._random_delay(0.5, 1.5, seed)

            # Human-like mouse movement before submit
            self._human_like_mouse_movement(driver)

            # Submit form
            submit_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit'], button[type='submit']")
            submit_button.click()

            # Wait for results
            self._random_delay(2.0, 4.0, seed)

            WebDriverWait(driver, 30).until(
                lambda d: d.execute_script('return document.readyState') == 'complete'
            )

            # Human-like scrolling
            self._human_like_scroll(driver, seed)

            # Extract results
            html = driver.page_source
            soup = BeautifulSoup(html, 'html5lib')
            results = self._extract_data(soup, 1)

            # Add search parameters to results
            for result in results:
                result['search_type'] = 'address'
                result['search_address'] = address
                if borough:
                    result['borough'] = borough

            return results

        finally:
            driver.quit()

    def search_by_party_name(self, party_name: str, document_type: Optional[str] = None, seed: Optional[int] = None) -> List[Dict]:
        """
        Search ACRIS by party name (grantor/grantee)

        Args:
            party_name: Name to search for
            document_type: Optional document type filter
            seed: Random seed for timing
        """
        if seed is None:
            seed = self.master_seed

        url = f"{self.ACRIS_BASE_URL}?menuchoice=NAME"
        results = []

        driver = self._create_driver()

        try:
            # Random delay before starting
            self._random_delay(1.0, 3.0, seed)

            driver.get(url)

            # Human-like mouse movement
            self._human_like_mouse_movement(driver)

            # Random delay after page load
            self._random_delay(2.0, 5.0, seed)

            # Check for CAPTCHA
            self._handle_captcha(driver, seed)

            # Wait for form to load
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.NAME, "name"))
            )

            # Fill in party name
            name_input = driver.find_element(By.NAME, "name")
            name_input.clear()
            name_input.send_keys(party_name)
            self._random_delay(0.5, 1.5, seed)

            # Select document type if provided
            if document_type:
                doc_type_select = Select(driver.find_element(By.NAME, "doc_type"))
                doc_type_select.select_by_value(document_type)
                self._random_delay(0.5, 1.5, seed)

            # Human-like mouse movement before submit
            self._human_like_mouse_movement(driver)

            # Submit form
            submit_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit'], button[type='submit']")
            submit_button.click()

            # Wait for results
            self._random_delay(2.0, 4.0, seed)

            WebDriverWait(driver, 30).until(
                lambda d: d.execute_script('return document.readyState') == 'complete'
            )

            # Human-like scrolling
            self._human_like_scroll(driver, seed)

            # Extract results
            html = driver.page_source
            soup = BeautifulSoup(html, 'html5lib')
            results = self._extract_data(soup, 1)

            # Add search parameters to results
            for result in results:
                result['search_type'] = 'party_name'
                result['search_name'] = party_name
                if document_type:
                    result['document_type'] = document_type

            return results

        finally:
            driver.quit()

    def search_by_document_id(self, document_id: str, seed: Optional[int] = None) -> Dict:
        """
        Search ACRIS by document ID

        Args:
            document_id: ACRIS document ID
            seed: Random seed for timing
        """
        if seed is None:
            seed = self.master_seed

        url = f"{self.ACRIS_BASE_URL}?menuchoice=DOC"
        result = {}

        driver = self._create_driver()

        try:
            # Random delay before starting
            self._random_delay(1.0, 3.0, seed)

            driver.get(url)

            # Human-like mouse movement
            self._human_like_mouse_movement(driver)

            # Random delay after page load
            self._random_delay(2.0, 5.0, seed)

            # Check for CAPTCHA
            self._handle_captcha(driver, seed)

            # Wait for form to load
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.NAME, "doc_id"))
            )

            # Fill in document ID
            doc_input = driver.find_element(By.NAME, "doc_id")
            doc_input.clear()
            doc_input.send_keys(document_id)
            self._random_delay(0.5, 1.5, seed)

            # Human-like mouse movement before submit
            self._human_like_mouse_movement(driver)

            # Submit form
            submit_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit'], button[type='submit']")
            submit_button.click()

            # Wait for results
            self._random_delay(2.0, 4.0, seed)

            WebDriverWait(driver, 30).until(
                lambda d: d.execute_script('return document.readyState') == 'complete'
            )

            # Human-like scrolling
            self._human_like_scroll(driver, seed)

            # Extract results
            html = driver.page_source
            soup = BeautifulSoup(html, 'html5lib')
            results = self._extract_data(soup, 1)

            if results:
                result = results[0]  # Document ID search returns single result
                result['search_type'] = 'document_id'
                result['document_id'] = document_id

            return result

        finally:
            driver.quit()

    def _parse_address(self, address: str) -> Dict[str, str]:
        """Parse address into components"""
        parts = {
            'street': '',
            'house_number': ''
        }

        # Extract house number (digits at start)
        match = re.match(r'^(\d+)\s+(.+)', address.strip())
        if match:
            parts['house_number'] = match.group(1)
            parts['street'] = match.group(2)
        else:
            parts['street'] = address.strip()

        return parts

    def search_multiple_blocks_lots(self, searches: List[Dict[str, str]], max_workers: int = 3) -> List[Dict]:
        """
        Search multiple block/lot combinations in parallel

        Args:
            searches: List of dicts with 'borough', 'block', 'lot' keys
            max_workers: Maximum parallel workers
        """
        master_seed = self._generate_seed_from_time()
        print(f"Searching {len(searches)} block/lot combinations with seed: {master_seed}")

        all_results = []

        # Limit workers to avoid detection
        workers = min(max_workers, len(searches), 5)

        with ThreadPoolExecutor(max_workers=workers) as executor:
            # Submit all search tasks
            future_to_search = {
                executor.submit(
                    self.search_by_block_lot,
                    search['borough'],
                    search['block'],
                    search['lot'],
                    master_seed + idx
                ): (idx, search)
                for idx, search in enumerate(searches)
            }

            # Process completed tasks with delays
            completed = 0
            for future in as_completed(future_to_search):
                idx, search = future_to_search[future]
                try:
                    results = future.result()
                    all_results.extend(results)
                    completed += 1
                    print(f"Completed search {idx+1}/{len(searches)}: Block {search['block']}, Lot {search['lot']} - {len(results)} records")

                    # Random delay between completions
                    if completed < len(searches):
                        self._random_delay(3.0, 8.0, master_seed + completed)

                except Exception as e:
                    print(f"Error searching Block {search['block']}, Lot {search['lot']}: {e}")
                    if "CAPTCHA" in str(e):
                        print("CAPTCHA detected - waiting 60 seconds...")
                        time.sleep(60)

        print(f"Total records found: {len(all_results)}")
        return all_results


if __name__ == "__main__":
    # Example usage
    scraper = ACRISScraper()

    # Search by block and lot
    print("Searching by Block/Lot...")
    results = scraper.search_by_block_lot(
        borough="1",  # Manhattan
        block="123",
        lot="45"
    )
    print(f"Found {len(results)} records")

    # Search by address
    print("\nSearching by Address...")
    results = scraper.search_by_address(
        address="123 Main Street",
        borough="1"  # Manhattan
    )
    print(f"Found {len(results)} records")

    # Search by party name
    print("\nSearching by Party Name...")
    results = scraper.search_by_party_name("Kettler")
    print(f"Found {len(results)} records")

    # Parallel search multiple blocks/lots
    print("\nParallel searching multiple blocks/lots...")
    searches = [
        {"borough": "1", "block": "123", "lot": "45"},
        {"borough": "1", "block": "124", "lot": "46"},
        {"borough": "2", "block": "200", "lot": "10"},
    ]
    results = scraper.search_multiple_blocks_lots(searches, max_workers=2)
    print(f"Total records found: {len(results)}")
